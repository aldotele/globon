import asyncio
import logging
import time

import aiohttp
from asgiref.sync import sync_to_async

from country.util.country_utils import CountryUtils
from country.util.factbook_extractor import FactbookExtractor
from world_proxy import proxy


def oneTimeIso2Update():
    from country.models import Country
    df_codesxref = proxy.retrieve_factbook_codesxref()
    for index, row in df_codesxref.iterrows():
        # gec code is used for factbook (e.g. gm for germany)
        gec = row['GEC'].lower()
        # iso3 code is used for restcountries and worldbank
        iso3 = row['A2']
        iso2 = row['A3']

        try:
            country = Country.objects.get(iso3=iso3)
            country.iso2 = iso2
            country.save()
        except:
            print("error on " + iso3 + "|" + iso2)


async def load_countries():
    # locale is used to parse as numbers strings written in this format "1,500.57"
    #locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    # first step is retrieving the codes of the country from factbook
    # different codes will be used to make proxy requests to different sources
    start_time = time.time()
    logging.info("loading country tables ...")
    df_codesxref = proxy.retrieve_factbook_codesxref()
    df_codes = proxy.retrieve_factbook_codes()

    async with aiohttp.ClientSession() as session:
        tasks = []
        parsed_iso3 = []

        for index, row in df_codesxref.iterrows():
            # gec code is used for factbook (e.g. gm for germany)
            gec = row['GEC'].lower()
            # iso3 code is used for restcountries and worldbank
            iso3 = row['A2']
            iso2 = row['A3']

            # persist country codes when relative factbook json is present
            if len(iso3) == 3 and iso3 not in parsed_iso3:
                parsed_iso3.append(iso3)
                region_search = df_codes.loc[df_codes['Code'] == gec, 'Region']
                if not region_search.empty:
                    # "&" and "and" will be replaced by "n" in region names
                    region = region_search.values[0].lower()\
                        .replace(" ", "-").replace("-and-", "-n-").replace("-&-", "-n-")

                    task = asyncio.ensure_future(proxy.retrieve_factbook_country(
                        session, iso3, iso2, gec.lower(), region)
                    )
                    tasks.append(task)

        results = await asyncio.gather(*tasks)

        for country_json in results:
            await load_country(country_json)

    end_time = time.time()
    logging.info("loading took " + str(start_time - end_time))


@sync_to_async()
def load_country(country_json):
    from country.models import Country, CountryGeography, CountryBorder, CountrySociety, CountryEconomy

    # Extraction
    iso3 = country_json['iso3']
    iso2 = country_json['iso2']
    gec = country_json['gec']
    income_level = CountryUtils.iso3_to_income.get(iso3, None)
    name = FactbookExtractor.extract_field(country_json['country'],
                                           'Government', 'Country name', 'conventional short form', 'text')
    official_name = FactbookExtractor.extract_field(country_json['country'],
                                                    'Government', 'Country name', 'conventional long form', 'text')
    # TODO use pattern instead, to catch the number which refers to population
    population = FactbookExtractor.parse_number(
        FactbookExtractor.extract_by(
            FactbookExtractor.extract_field(country_json['country'], "People and Society", "Population", "text"),
            until=" "
        )
    )
    gdp_real = FactbookExtractor.parse_number(
        FactbookExtractor.extract_by(
            FactbookExtractor.extract_most_recent_field(country_json['country'],
                                                        'Economy', 'Real GDP (purchasing power parity)'),
            delimiters=("$", "(")
        ),
        with_unit=True
    )
    gdp_gross = FactbookExtractor.parse_number(
        FactbookExtractor.extract_by(
            FactbookExtractor.extract_field(country_json['country'],
                                            'Economy', 'GDP (official exchange rate)', 'text'),
            delimiters=("$", "(")
        ),
        with_unit=True
    )
    real_gdp_growth_rate = FactbookExtractor.parse_number(
        FactbookExtractor.extract_by(
            FactbookExtractor.extract_most_recent_field(country_json['country'],
                                                        'Economy', 'Real GDP growth rate'),
            until="%"
        )
    )
    real_gdp_per_capita = FactbookExtractor.parse_number(
        FactbookExtractor.extract_by(
            FactbookExtractor.extract_most_recent_field(country_json['country'],
                                                        'Economy', 'Real GDP per capita'),
            delimiters=("$", " ")
        )
    )
    inflation_rate = FactbookExtractor.parse_number(
        FactbookExtractor.extract_by(
            FactbookExtractor.extract_most_recent_field(country_json['country'],
                                                        'Economy', 'Inflation rate (consumer prices)'),
            until="%"
        )
    )
    labor_force = FactbookExtractor.parse_number(
        FactbookExtractor.extract_by(
            FactbookExtractor.extract_field(country_json['country'],
                                            'Economy', 'Labor force', 'text'),
            until="("
        ),
        with_unit=True
    )
    unemployment_rate = FactbookExtractor.parse_number(
        FactbookExtractor.extract_by(
            FactbookExtractor.extract_most_recent_field(country_json['country'],
                                                        'Economy', 'Unemployment rate'),
            until="%"
        )
    )
    public_debt = FactbookExtractor.parse_number(
        FactbookExtractor.extract_by(
            FactbookExtractor.extract_most_recent_field(country_json['country'],
                                                        'Economy', 'Public debt'),
            until="%"
        )
    )
    exports = FactbookExtractor.parse_number(
        FactbookExtractor.extract_by(
            FactbookExtractor.extract_most_recent_field(country_json['country'],
                                                        'Economy', 'Exports'),
            delimiters=("$", "(")
        ),
        with_unit=True
    )
    imports = FactbookExtractor.parse_number(
        FactbookExtractor.extract_by(
            FactbookExtractor.extract_most_recent_field(country_json['country'],
                                                        'Economy', 'Imports'),
            delimiters=("$", "(")
        ),
        with_unit=True
    )
    capital = FactbookExtractor.extract_capital(country_json['country'], "Government", "Capital", "name", "text")
    border_countries_dict = FactbookExtractor.extract_border_countries(country_json['country'],
                                                                       "Geography", "Land boundaries",
                                                                       "border countries", "text")
    lat_lng = FactbookExtractor.extract_coordinates(country_json['country'],
                                                    "Geography", "Geographic coordinates", "text")
    flag = FactbookExtractor.extract_flag(country_json['gec'])
    maps = FactbookExtractor.extract_map(country_json['gec'])
    total_area_sq_km = FactbookExtractor.parse_number(
        FactbookExtractor.extract_by(
            FactbookExtractor.extract_field(country_json['country'], "Geography", "Area", "total", "text"),
            until=" sq"
        )
    )
    land_area_sq_km = FactbookExtractor.parse_number(
        FactbookExtractor.extract_by(
            FactbookExtractor.extract_field(country_json['country'], "Geography", "Area", "land", "text"),
            until=" sq"
        )
    )
    water_area_sq_km = FactbookExtractor.parse_number(
        FactbookExtractor.extract_by(
            FactbookExtractor.extract_field(country_json['country'], "Geography", "Area", "water", "text"),
            until=" sq"
        )
    )
    border_length_km = FactbookExtractor.parse_number(
        FactbookExtractor.extract_by(
            FactbookExtractor.extract_field(country_json['country'], "Geography", "Land boundaries", "total", "text"),
            until=" km"
        )
    )
    coastline_length_km = FactbookExtractor.parse_number(
        FactbookExtractor.extract_by(
            FactbookExtractor.extract_field(country_json['country'], "Geography", "Coastline", "text"),
            until=" km"
        )
    )
    population_growth_rate = FactbookExtractor.parse_number(
        FactbookExtractor.extract_by(
            FactbookExtractor.extract_field(country_json['country'],
                                            'People and Society', 'Population growth rate', "text"),
            until="%"
        )
    )
    population_0_14_percentage = FactbookExtractor.parse_number(
        FactbookExtractor.extract_by(
            FactbookExtractor.extract_field(country_json['country'],
                                            'People and Society', 'Age structure', '0-14 years', "text"),
            until="%"
        )
    )
    population_15_64_percentage = FactbookExtractor.parse_number(
        FactbookExtractor.extract_by(
            FactbookExtractor.extract_field(country_json['country'],
                                            'People and Society', 'Age structure', '15-64 years', "text"),
            until="%"
        )
    )
    population_65_more_percentage = FactbookExtractor.parse_number(
        FactbookExtractor.extract_by(
            FactbookExtractor.extract_field(country_json['country'],
                                            'People and Society', 'Age structure', '65 years and over', "text"),
            until="%"
        )
    )

    median_age = FactbookExtractor.parse_number(
        FactbookExtractor.extract_by(
            FactbookExtractor.extract_field(country_json['country'],
                                            'People and Society', 'Median age', 'total', "text"),
            until="years"
        )
    )

    median_age_male = FactbookExtractor.parse_number(
        FactbookExtractor.extract_by(
            FactbookExtractor.extract_field(country_json['country'],
                                            'People and Society', 'Median age', 'male', "text"),
            until="years"
        )
    )
    median_age_female = FactbookExtractor.parse_number(
        FactbookExtractor.extract_by(
            FactbookExtractor.extract_field(country_json['country'],
                                            'People and Society', 'Median age', 'female', "text"),
            until="years"
        )
    )
    births_every_1000 = FactbookExtractor.parse_number(
        FactbookExtractor.extract_by(
            FactbookExtractor.extract_field(country_json['country'],
                                            'People and Society', 'Birth rate', "text"),
            until="births"
        )
    )
    deaths_every_1000 = FactbookExtractor.parse_number(
        FactbookExtractor.extract_by(
            FactbookExtractor.extract_field(country_json['country'],
                                            'People and Society', 'Death rate', "text"),
            until="deaths"
        )
    )
    migrants_every_1000 = FactbookExtractor.parse_number(
        FactbookExtractor.extract_by(
            FactbookExtractor.extract_field(country_json['country'],
                                            'People and Society', 'Net migration rate', "text"),
            until="migrant"
        )
    )
    urban_population_percentage = FactbookExtractor.parse_number(
        FactbookExtractor.extract_by(
            FactbookExtractor.extract_field(country_json['country'],
                                            'People and Society', 'Urbanization', 'urban population', "text"),
            until="%"
        )
    )
    life_expectancy_at_birth = FactbookExtractor.parse_number(
        FactbookExtractor.extract_by(
            FactbookExtractor.extract_field(country_json['country'],
                                            'People and Society', 'Life expectancy at birth',
                                            'total population', "text"),
            until="years"
        )
    )
    life_expectancy_at_birth_male = FactbookExtractor.parse_number(
        FactbookExtractor.extract_by(
            FactbookExtractor.extract_field(country_json['country'],
                                            'People and Society', 'Life expectancy at birth',
                                            'male', "text"),
            until="years"
        )
    )
    life_expectancy_at_birth_female = FactbookExtractor.parse_number(
        FactbookExtractor.extract_by(
            FactbookExtractor.extract_field(country_json['country'],
                                            'People and Society', 'Life expectancy at birth',
                                            'female', "text"),
            until="years"
        )
    )
    births_per_woman = FactbookExtractor.parse_number(
        FactbookExtractor.extract_by(
            FactbookExtractor.extract_field(country_json['country'],
                                            'People and Society', 'Total fertility rate', "text"),
            until="children"
        )
    )
    health_expenditure = FactbookExtractor.parse_number(
        FactbookExtractor.extract_by(
            FactbookExtractor.extract_field(country_json['country'],
                                            'People and Society', 'Current health expenditure', "text"),
            until="%"
        )
    )
    physicians_density = FactbookExtractor.parse_number(
        FactbookExtractor.extract_by(
            FactbookExtractor.extract_field(country_json['country'],
                                            'People and Society', 'Physicians density', "text"),
            until="physicians"
        )
    )
    hospital_bed_density = FactbookExtractor.parse_number(
        FactbookExtractor.extract_by(
            FactbookExtractor.extract_field(country_json['country'],
                                            'People and Society', 'Hospital bed density', "text"),
            until="beds"
        )
    )
    obesity_rate = FactbookExtractor.parse_number(
        FactbookExtractor.extract_by(
            FactbookExtractor.extract_field(country_json['country'],
                                            'People and Society', 'Obesity - adult prevalence rate', "text"),
            until="%"
        )
    )
    alcohol_consumption_per_capita = FactbookExtractor.parse_number(
        FactbookExtractor.extract_by(
            FactbookExtractor.extract_field(country_json['country'],
                                            'People and Society', 'Alcohol consumption per capita', 'total', "text"),
            until="liters"
        )
    )
    beer_consumption_per_capita = FactbookExtractor.parse_number(
        FactbookExtractor.extract_by(
            FactbookExtractor.extract_field(country_json['country'],
                                            'People and Society', 'Alcohol consumption per capita', 'beer', "text"),
            until="liters"
        )
    )
    wine_consumption_per_capita = FactbookExtractor.parse_number(
        FactbookExtractor.extract_by(
            FactbookExtractor.extract_field(country_json['country'],
                                            'People and Society', 'Alcohol consumption per capita', 'wine', "text"),
            until="liters"
        )
    )
    spirits_consumption_per_capita = FactbookExtractor.parse_number(
        FactbookExtractor.extract_by(
            FactbookExtractor.extract_field(country_json['country'],
                                            'People and Society', 'Alcohol consumption per capita', 'spirits', "text"),
            until="liters"
        )
    )
    tobacco_use = FactbookExtractor.parse_number(
        FactbookExtractor.extract_by(
            FactbookExtractor.extract_field(country_json['country'],
                                            'People and Society', 'Tobacco use', 'total', "text"),
            until="liters"
        )
    )
    tobacco_use_male = FactbookExtractor.parse_number(
        FactbookExtractor.extract_by(
            FactbookExtractor.extract_field(country_json['country'],
                                            'People and Society', 'Tobacco use', 'male', "text"),
            until="liters"
        )
    )
    tobacco_use_female = FactbookExtractor.parse_number(
        FactbookExtractor.extract_by(
            FactbookExtractor.extract_field(country_json['country'],
                                            'People and Society', 'Tobacco use', 'female', "text"),
            until="liters"
        )
    )
    married_women_rate = FactbookExtractor.parse_number(
        FactbookExtractor.extract_by(
            FactbookExtractor.extract_field(country_json['country'],
                                            'People and Society', 'Currently married women (ages 15-49)', "text"),
            until="%"
        )
    )
    literacy_rate = FactbookExtractor.parse_number(
        FactbookExtractor.extract_by(
            FactbookExtractor.extract_field(country_json['country'],
                                            'People and Society', 'Literacy', 'total population', "text"),
            until="%"
        )
    )
    literacy_rate_male = FactbookExtractor.parse_number(
        FactbookExtractor.extract_by(
            FactbookExtractor.extract_field(country_json['country'],
                                            'People and Society', 'Literacy', 'male', "text"),
            until="%"
        )
    )
    literacy_rate_female = FactbookExtractor.parse_number(
        FactbookExtractor.extract_by(
            FactbookExtractor.extract_field(country_json['country'],
                                            'People and Society', 'Literacy', 'female', "text"),
            until="%"
        )
    )
    gdp_agriculture = FactbookExtractor.parse_number(
        FactbookExtractor.extract_by(
            FactbookExtractor.extract_field(country_json['country'],
                                            'Economy', 'GDP - composition, by sector of origin', 'agriculture', 'text'),
            until="%"
        )
    )
    gdp_industry = FactbookExtractor.parse_number(
        FactbookExtractor.extract_by(
            FactbookExtractor.extract_field(country_json['country'],
                                            'Economy', 'GDP - composition, by sector of origin', 'industry', 'text'),
            until="%"
        )
    )
    gdp_services = FactbookExtractor.parse_number(
        FactbookExtractor.extract_by(
            FactbookExtractor.extract_field(country_json['country'],
                                            'Economy', 'GDP - composition, by sector of origin', 'services', 'text'),
            until="%"
        )
    )
    industrial_production_growth_rate = FactbookExtractor.parse_number(
        FactbookExtractor.extract_by(
            FactbookExtractor.extract_field(country_json['country'],
                                            'Economy', 'Industrial production growth rate', 'text'),
            until="%"
        )
    )
    labor_force_agriculture = FactbookExtractor.parse_number(
        FactbookExtractor.extract_by(
            FactbookExtractor.extract_field(country_json['country'],
                                            'Economy', 'Labor force - by occupation', 'agriculture', 'text'),
            until="%"
        )
    )
    labor_force_industry = FactbookExtractor.parse_number(
        FactbookExtractor.extract_by(
            FactbookExtractor.extract_field(country_json['country'],
                                            'Economy', 'Labor force - by occupation', 'industry', 'text'),
            until="%"
        )
    )
    labor_force_services = FactbookExtractor.parse_number(
        FactbookExtractor.extract_by(
            FactbookExtractor.extract_field(country_json['country'],
                                            'Economy', 'Labor force - by occupation', 'services', 'text'),
            until="%"
        )
    )
    unemployment_rate_youth = FactbookExtractor.parse_number(
        FactbookExtractor.extract_by(
            FactbookExtractor.extract_field(country_json['country'],
                                            'Economy', 'Youth unemployment rate (ages 15-24)', 'total', 'text'),
            until="%"
        )
    )
    population_below_poverty_line = FactbookExtractor.parse_number(
        FactbookExtractor.extract_by(
            FactbookExtractor.extract_field(country_json['country'],
                                            'Economy', 'Population below poverty line', 'text'),
            until="%"
        )
    )
    taxes = FactbookExtractor.parse_number(
        FactbookExtractor.extract_by(
            FactbookExtractor.extract_field(country_json['country'],
                                            'Economy', 'Taxes and other revenues', 'text'),
            until="%"
        )
    )

    # actual database loading starts here
    country = Country.objects.create(
        iso3=iso3,
        iso2=iso2,
        gec=gec,
        name=name if name != "none" else official_name if official_name else None,
        official_name=official_name if official_name != "none" else None,
        capital=capital,
        flag=flag,
        income_level=income_level
    )

    CountryGeography.objects.create(
        country=country,
        maps=maps,
        total_area_sq_km=total_area_sq_km,
        land_area_sq_km=land_area_sq_km,
        water_area_sq_km=water_area_sq_km,
        border_length_km=border_length_km,
        coastline_length_km=coastline_length_km,
        lat_lng=lat_lng
    )

    CountrySociety.objects.create(
        country=country,
        population=population,
        population_growth_rate=population_growth_rate,
        population_0_14_percentage=population_0_14_percentage,
        population_15_64_percentage=population_15_64_percentage,
        population_65_more_percentage=population_65_more_percentage,
        births_every_1000=births_every_1000,
        deaths_every_1000=deaths_every_1000,
        median_age=median_age,
        median_age_male=median_age_male,
        median_age_female=median_age_female,
        migrants_every_1000=migrants_every_1000,
        urban_population_percentage=urban_population_percentage,
        life_expectancy_at_birth=life_expectancy_at_birth,
        life_expectancy_at_birth_male=life_expectancy_at_birth_male,
        life_expectancy_at_birth_female=life_expectancy_at_birth_female,
        births_per_woman=births_per_woman,
        health_expenditure=health_expenditure,
        physicians_density=physicians_density,
        hospital_bed_density=hospital_bed_density,
        obesity_rate=obesity_rate,
        alcohol_consumption_per_capita=alcohol_consumption_per_capita,
        beer_consumption_per_capita=beer_consumption_per_capita,
        wine_consumption_per_capita=wine_consumption_per_capita,
        spirits_consumption_per_capita=spirits_consumption_per_capita,
        tobacco_use=tobacco_use,
        tobacco_use_male=tobacco_use_male,
        tobacco_use_female=tobacco_use_female,
        married_women_rate=married_women_rate,
        literacy_rate=literacy_rate,
        literacy_rate_male=literacy_rate_male,
        literacy_rate_female=literacy_rate_female
    )

    CountryEconomy.objects.create(
        country=country,
        gdp_agriculture=gdp_agriculture,
        gdp_industry=gdp_industry,
        gdp_services=gdp_services,
        industrial_production_growth_rate=industrial_production_growth_rate,
        labor_force=labor_force,
        labor_force_agriculture=labor_force_agriculture,
        labor_force_industry=labor_force_industry,
        labor_force_services=labor_force_services,
        unemployment_rate_youth=unemployment_rate_youth,
        population_below_poverty_line=population_below_poverty_line,
        taxes=taxes,
        inflation_rate=inflation_rate,
        gdp_real=gdp_real,
        gdp_gross=gdp_gross,
        real_gdp_growth_rate=real_gdp_growth_rate,
        real_gdp_per_capita=real_gdp_per_capita,
        imports=imports,
        exports=exports,
        unemployment_rate=unemployment_rate,
        public_debt=public_debt
    )

    for key in border_countries_dict:
        CountryBorder.objects.create(
            country1=name if name != "none" else official_name if official_name else None,
            country2=key,
            length_km=border_countries_dict[key]
        )

