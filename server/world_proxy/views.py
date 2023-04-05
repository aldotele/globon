from django.shortcuts import render
from django.http import HttpResponse
import requests
from world_proxy.models import Country


def welcome(request):
    return render(request, 'welcome.html')


def get_all_countries(request):
    # TODO add if/else
    # if countries are already in the db, retrieve from there
    # otherwise invoke the proxy to populate the db and to return the countries
    response = requests.get("https://restcountries.com/v3.1/all")

    #if 1 == 0:
    for country_in_json in response.json():
        country = Country()
        country.from_json(country_in_json)
        country.save()

    return HttpResponse(response, content_type='application/json')
