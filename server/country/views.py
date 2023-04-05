from django.shortcuts import render
from django.http import HttpResponse
import requests


def get_all_countries(request):
    # TODO add if/else
    # if countries are already in the db, retrieve from there
    # otherwise invoke the proxy to populate the db and to return the countries
    response = requests.get("https://restcountries.com/v3.1/all")

    return HttpResponse(response, content_type='application/json')