import asyncio
import logging
import time

import aiohttp
from asgiref.sync import sync_to_async

from country.util.factbook_extractor import FactbookExtractor
from world_proxy import proxy


async def load_country_data():
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
                    # invoking factbook
                    tasks.append(
                        asyncio.ensure_future(proxy.retrieve_factbook_country(session, iso3, gec.lower(), region))
                    )

        results = await asyncio.gather(*tasks)
        for country_json in results:
            await create_country(country_json)

    # TODO handle income loading
    # worldbank_countries = proxy.retrieve_worldbank_countries()
    # for country_details in worldbank_countries:
    #     Country.objects.filter(iso3=country_details["id"]).update(income_level=country_details["incomeLevel"]["id"])
    end_time = time.time()
    logging.info("loading took " + str(start_time - end_time))


@sync_to_async()
def create_country(country_json):
    from country.models import Country

    iso3 = country_json['iso3']
    name = country_json['country']['Government']['Country name']['conventional short form']['text']
    official_name = country_json['country']['Government']['Country name']['conventional long form']['text']
    population = FactbookExtractor.extract_population(country_json['country']['People and Society']['Population']['text'])
    capital = FactbookExtractor.extract_capital(country_json['country'], ["Government", "Capital", "name", "text"])
    flag = FactbookExtractor.extract_flag(country_json['gec'])
    map = FactbookExtractor.extract_flag(country_json['gec'])

    Country.objects.create(
        iso3=iso3,
        name=name if name != "none" else official_name if official_name else None,
        official_name=official_name if official_name != "none" else None,
        population=population, capital=capital,
        flag=flag,
        map=map
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
