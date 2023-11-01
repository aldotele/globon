import asyncio
import logging
import time

import aiohttp
from asgiref.sync import sync_to_async

from country.util.country_utils import CountryUtils
from country.util.factbook_extractor import FactbookExtractor
from world_proxy import proxy


async def load_countries():
    # first step is retrieving the codes of the country from factbook
    # different codes will be used to make proxy requests to different sources
    start_time = time.time()
    logging.info("loading country tables ...")
    df_codesxref = proxy.retrieve_factbook_codesxref()
    df_codes = proxy.retrieve_factbook_codes()

    async with aiohttp.ClientSession() as session:
        tasks = []

        for index, row in df_codesxref.iterrows():
            # gec code is used for factbook (e.g. gm for germany)
            gec = row['GEC'].lower()
            # iso3 code is used for restcountries and worldbank
            iso3 = row['A2']

            # persist country codes when relative factbook json is present
            if len(iso3) == 3:
                region_search = df_codes.loc[df_codes['Code'] == gec, 'Region']
                if not region_search.empty:
                    # "&" and "and" will be replaced by "n" in region names
                    region = region_search.values[0].lower()\
                        .replace(" ", "-").replace("-and-", "-n-").replace("-&-", "-n-")

                    # persisting the codes
                    await create_country_codes(iso3, gec.upper(), row)

                    task = asyncio.ensure_future(proxy.retrieve_factbook_country(session, iso3, gec.lower(), region))
                    tasks.append(task)

        results = await asyncio.gather(*tasks)

        for country_json in results:
            await load_country(country_json)

    end_time = time.time()
    logging.info("loading took " + str(start_time - end_time))


@sync_to_async()
def load_country(country_json):
    from country.models import Country, CountryGeography, CountryBorder, CountrySociety

    iso3 = country_json['iso3']
    name = country_json['country']['Government']['Country name']['conventional short form']['text']
    official_name = country_json['country']['Government']['Country name']['conventional long form']['text']
    population = FactbookExtractor.extract_population(
        country_json['country']['People and Society']['Population']['text'])
    capital = FactbookExtractor.extract_capital(country_json['country'], "Government", "Capital", "name", "text")
    flag = FactbookExtractor.extract_flag(country_json['gec'])
    map = FactbookExtractor.extract_flag(country_json['gec'])
    total_area_sq_km = FactbookExtractor.extract_area(country_json['country'], "Geography", "Area", "total", "text")
    land_area_sq_km = FactbookExtractor.extract_area(country_json['country'], "Geography", "Area", "land", "text")
    water_area_sq_km = FactbookExtractor.extract_area(country_json['country'], "Geography", "Area", "water", "text")
    border_length_km = FactbookExtractor.extract_length(country_json['country'],
                                                        "Geography", "Land boundaries", "total", "text")
    coastline_length_km = FactbookExtractor.extract_length(country_json['country'], "Geography", "Coastline", "text")
    border_countries_dict = FactbookExtractor.extract_border_countries(country_json['country'],
                                                                       "Geography", "Land boundaries",
                                                                       "border countries", "text")
    income_level = CountryUtils.iso3_to_income.get(iso3, None)
    lat_lng = FactbookExtractor.extract_coordinates(country_json['country'],
                                                    "Geography", "Geographic coordinates", "text")
    population_growth_rate = FactbookExtractor.extract_until_delimiter(country_json['country'], "%",
                                                                       'People and Society', 'Population growth rate',
                                                                       'text')
    population_0_14_percentage = FactbookExtractor.extract_until_delimiter(country_json['country'], "%",
                                                                           'People and Society', 'Age structure',
                                                                           '0-14 years', 'text')
    population_15_64_percentage = FactbookExtractor.extract_until_delimiter(country_json['country'], "%",
                                                                            'People and Society', 'Age structure',
                                                                            '15-64 years', 'text')
    population_65_more_percentage = FactbookExtractor.extract_until_delimiter(country_json['country'], "%",
                                                                              'People and Society', 'Age structure',
                                                                              '65 years and over', 'text')
    median_age = FactbookExtractor.extract_until_delimiter(country_json['country'], "years",
                                                           'People and Society', 'Median age', 'total', 'text')
    median_age_male = FactbookExtractor.extract_until_delimiter(country_json['country'], "years",
                                                                'People and Society', 'Median age', 'male', 'text')
    median_age_female = FactbookExtractor.extract_until_delimiter(country_json['country'], "years",
                                                                  'People and Society', 'Median age', 'female', 'text')
    births_every_1000 = FactbookExtractor.extract_until_delimiter(country_json['country'], "births",
                                                                  'People and Society', 'Birth rate', 'text')
    deaths_every_1000 = FactbookExtractor.extract_until_delimiter(country_json['country'], "deaths",
                                                                  'People and Society', 'Death rate', 'text')
    migrants_every_1000 = FactbookExtractor.extract_until_delimiter(country_json['country'], "migrant",
                                                                    'People and Society', 'Net migration rate', 'text')
    urban_population_percentage = FactbookExtractor.extract_until_delimiter(country_json['country'], "%",
                                                                            'People and Society', 'Urbanization',
                                                                            'urban population', 'text')
    life_expectancy_at_birth = FactbookExtractor.extract_until_delimiter(country_json['country'], "years",
                                                                         'People and Society',
                                                                         'Life expectancy at birth',
                                                                         'total population', 'text')
    life_expectancy_at_birth_male = FactbookExtractor.extract_until_delimiter(country_json['country'], "years",
                                                                              'People and Society',
                                                                              'Life expectancy at birth',
                                                                              'male', 'text')
    life_expectancy_at_birth_female = FactbookExtractor.extract_until_delimiter(country_json['country'], "years",
                                                                                'People and Society',
                                                                                'Life expectancy at birth',
                                                                                'female', 'text')
    births_per_woman = FactbookExtractor.extract_until_delimiter(country_json['country'], "children",
                                                                 'People and Society',
                                                                 'Total fertility rate', 'text')
    health_expenditure = FactbookExtractor.extract_until_delimiter(country_json['country'], "%",
                                                                   'People and Society',
                                                                   'Current health expenditure', 'text')
    physicians_density = FactbookExtractor.extract_until_delimiter(country_json['country'], "physicians",
                                                                   'People and Society',
                                                                   'Physicians density', 'text')
    hospital_bed_density = FactbookExtractor.extract_until_delimiter(country_json['country'], "beds",
                                                                     'People and Society',
                                                                     'Hospital bed density', 'text')
    obesity_rate = FactbookExtractor.extract_until_delimiter(country_json['country'], "%",
                                                             'People and Society',
                                                             'Obesity - adult prevalence rate', 'text')
    alcohol_consumption_per_capita = FactbookExtractor.extract_until_delimiter(country_json['country'], "liters",
                                                                               'People and Society',
                                                                               'Alcohol consumption per capita',
                                                                               'total', 'text')
    beer_consumption_per_capita = FactbookExtractor.extract_until_delimiter(country_json['country'], "liters",
                                                                            'People and Society',
                                                                            'Alcohol consumption per capita',
                                                                            'beer', 'text')
    wine_consumption_per_capita = FactbookExtractor.extract_until_delimiter(country_json['country'], "liters",
                                                                            'People and Society',
                                                                            'Alcohol consumption per capita',
                                                                            'wine', 'text')
    spirits_consumption_per_capita = FactbookExtractor.extract_until_delimiter(country_json['country'], "liters",
                                                                               'People and Society',
                                                                               'Alcohol consumption per capita',
                                                                               'spirits', 'text')
    tobacco_use = FactbookExtractor.extract_until_delimiter(country_json['country'], "%",
                                                            'People and Society',
                                                            'Tobacco use', 'total', 'text')
    tobacco_use_male = FactbookExtractor.extract_until_delimiter(country_json['country'], "%",
                                                                 'People and Society',
                                                                 'Tobacco use', 'male', 'text')
    tobacco_use_female = FactbookExtractor.extract_until_delimiter(country_json['country'], "%",
                                                                   'People and Society',
                                                                   'Tobacco use', 'female', 'text')
    married_women_rate = FactbookExtractor.extract_until_delimiter(country_json['country'], "%",
                                                                   'People and Society',
                                                                   'Currently married women (ages 15-49)', 'text')
    literacy_rate = FactbookExtractor.extract_until_delimiter(country_json['country'], "%",
                                                              'People and Society',
                                                              'Literacy', 'total population', 'text')
    literacy_rate_male = FactbookExtractor.extract_until_delimiter(country_json['country'], "%",
                                                                   'People and Society',
                                                                   'Literacy', 'male', 'text')
    literacy_rate_female = FactbookExtractor.extract_until_delimiter(country_json['country'], "%",
                                                                     'People and Society',
                                                                     'Literacy', 'female', 'text')

    Country.objects.create(
        iso3=iso3,
        name=name if name != "none" else official_name if official_name else None,
        official_name=official_name if official_name != "none" else None,
        capital=capital,
        flag=flag,
        map=map,
        income_level=income_level
    )

    CountryGeography.objects.create(
        iso3=iso3,
        total_area_sq_km=total_area_sq_km,
        land_area_sq_km=land_area_sq_km,
        water_area_sq_km=water_area_sq_km,
        border_length_km=border_length_km,
        coastline_length_km=coastline_length_km,
        lat_lng=lat_lng
    )

    CountrySociety.objects.create(
        iso3=iso3,
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

    for key in border_countries_dict:
        CountryBorder.objects.create(
            country1=name if name != "none" else official_name if official_name else None,
            country2=key,
            length_km=border_countries_dict[key]
        )


@sync_to_async
def create_country_codes(iso3, gec, codes):
    from country.models import CountryCodes
    CountryCodes.objects.create(
        name=codes['Name'],
        gec=gec,
        iso2=codes['A3'],
        iso3=iso3,
        stanag=codes['STANAG'],
        internet=codes['INTERNET']
    )
