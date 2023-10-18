import asyncio
import logging
import time

import aiohttp
from asgiref.sync import sync_to_async

from country.util.country_utils import CountryUtils
from world_proxy import proxy


async def load_country_data():
    # first step is retrieving the codes of the country from factbook
    # different codes will be used to make proxy requests to different sources
    start_time = time.time()
    logging.info("loading country tables ...")
    df = proxy.retrieve_factbook_codes()

    async with aiohttp.ClientSession() as session:
        tasks = []

        for index, row in df.iterrows():
            # gec code is used for factbook (e.g. gm for germany)
            gec = row['GEC']
            # iso3 code is used for restcountries and worldbank
            iso3 = row['A2']

            # persist country codes when relative factbook json is present
            if gec.lower() in CountryUtils.gec_to_continent and (iso3 in CountryUtils.restcountries_iso3 or iso3 == 'XKS'):
                # persisting the codes
                await create_country_codes(iso3, gec, row)
                continent = CountryUtils.gec_to_continent[gec.lower()]

                tasks.append(asyncio.ensure_future(proxy.retrieve_factbook_country(session, gec.lower(), continent)))
                # invoke restcountries handling the Kosovo inconsistency
                #restcountries_country_json = proxy.retrieve_restcountries_country(iso3 if iso3 != "XKS" else "UNK")

                # TODO find a way to extract properly population from factbook
                # population = extract_factbook_population(country_json['People and Society']['Population']['text'])

        res = await asyncio.gather(*tasks)
        for country in res:
            await create_country(None, country, None)

    # TODO handle income loading
    # worldbank_countries = proxy.retrieve_worldbank_countries()
    # for country_details in worldbank_countries:
    #     Country.objects.filter(iso3=country_details["id"]).update(income_level=country_details["incomeLevel"]["id"])
    end_time = time.time()
    logging.info("loading took " + str(start_time - end_time))


@sync_to_async()
def create_country(iso3, factbook_country_json, restcountries_country_json):
    from country.models import Country

    name = factbook_country_json['Government']['Country name']['conventional short form']['text']
    official_name = factbook_country_json['Government']['Country name']['conventional long form']['text']
    # population = restcountries_country_json['population'] if restcountries_country_json else None
    # capital = restcountries_country_json['capital'] if 'capital' in restcountries_country_json else None
    # flag = restcountries_country_json['flags']['svg'] if restcountries_country_json else None
    # map = restcountries_country_json['maps']['openStreetMaps'] if 'maps' in restcountries_country_json else None
    # borders = restcountries_country_json['borders'] if 'borders' in restcountries_country_json else None
    # currencies = Country.retrieve_currencies(restcountries_country_json['currencies']) if 'currencies' in restcountries_country_json else None
    # languages = Country.retrieve_languages(restcountries_country_json['languages']) if 'languages' in restcountries_country_json else None

    Country.objects.create(
        name=name,
        official_name=official_name if official_name != "none" else None,
        iso3=name[:3],
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
