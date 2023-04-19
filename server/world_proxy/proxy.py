import requests


def retrieve_all_countries():
    response = requests.get("https://restcountries.com/v3.1/all")
    return response.json()


def retrieve_world_bank_country_details():
    response = requests.get("https://api.worldbank.org/v2/country?format=json&per_page=299")
    return response.json()[1]

