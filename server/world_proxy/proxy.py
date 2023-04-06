import requests


def retrieve_all_countries():
    response = requests.get("https://restcountries.com/v3.1/all")
    return response.json()
