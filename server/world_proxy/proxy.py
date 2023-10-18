import pandas as pd
import requests


class ProxyAPI:
    factbook_codes = "https://raw.githubusercontent.com/factbook/factbook/master/factbook-codes/data/codesxref.csv"
    factbook_country_base_uri = "https://raw.githubusercontent.com/factbook/factbook.json/master"
    restcountries_base_uri = "https://restcountries.com/v3.1"
    worldbank_uri = "https://api.worldbank.org/v2/country?format=json&per_page=299"


def retrieve_restcountries_all():
    response = requests.get(ProxyAPI.restcountries_base_uri + "/all")
    return response.json()


async def retrieve_restcountries_country(session, iso3):
    async with session.get(ProxyAPI.restcountries_base_uri + "/alpha/" + iso3) as resp:
        country_json = await resp.json()
        return country_json[0]


def retrieve_worldbank_countries():
    response = requests.get(ProxyAPI.worldbank_uri)
    return response.json()[1]


def retrieve_factbook_codes():
    return pd.read_csv(ProxyAPI.factbook_codes, na_filter=False)


async def retrieve_factbook_country(session, gec, continent):
    async with session.get(ProxyAPI.factbook_country_base_uri + "/" + continent + "/" + gec + ".json") as resp:
        country_json = await resp.json(content_type=None)
        return country_json