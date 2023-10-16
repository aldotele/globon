import asyncio
import time

from asgiref.sync import sync_to_async

from country.util.country_utils import CountryUtils
from world_proxy import proxy


async def load_country_data():
    # first step is retrieving the codes of the country from factbook
    # different codes will be used to make proxy requests to different sources
    df = proxy.retrieve_factbook_codes()
    start_time = time.time()
    for index, row in df.iterrows():
        # gec code is used for factbook (e.g. gm for germany)
        gec = row['GEC']
        # iso3 code is used for restcountries and worldbank
        iso3 = row['A2']

        # persist country codes when relative factbook json is present
        if gec.lower() in CountryUtils.gec_to_continent and len(iso3) == 3 and iso3 != "XKS":
            country_codes_task = asyncio.create_task(create_country_codes(iso3, gec, row))
            continent = CountryUtils.gec_to_continent[gec.lower()]
            # run asynchronous proxy requests
            factbook_task = asyncio.create_task(from_factbook(gec.lower(), continent))
            restcountries_task = asyncio.create_task(from_restcountries(iso3))

            await factbook_task, restcountries_task

            factbook_country_json = factbook_task.result()
            restcountries_country_json = restcountries_task.result()

            # TODO find a way to extract properly population from factbook
            #population = extract_factbook_population(country_json['People and Society']['Population']['text'])
            await create_country(iso3, factbook_country_json, restcountries_country_json)
            await country_codes_task
    end_time = time.time()
    print(end_time - start_time)


async def from_factbook(gec, continent):
    # Simulate an asynchronous request to retrieve JSON
    return proxy.retrieve_factbook_country(gec, continent)


async def from_restcountries(iso3):
    return proxy.retrieve_restcountries_country(iso3)


@sync_to_async
def create_country(iso3, factbook_country_json, restcountries_country_json):
    from country.models import Country
    Country.objects.create(
        name=factbook_country_json['Government']['Country name']['conventional short form']['text'],
        official_name=factbook_country_json['Government']['Country name']['conventional long form']['text'],
        iso3=iso3,
        population=restcountries_country_json['population'],
        #capital=restcountries_country_json['capital'],  # TODO handle Key Error
        flag=restcountries_country_json['flags']['svg'],
        map=restcountries_country_json['maps']['openStreetMaps'],
        #borders=restcountries_country_json['borders']  # TODO handle Key Error
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
    return "ok"
