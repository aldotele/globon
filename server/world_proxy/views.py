from django.shortcuts import render
import requests
from django.http import HttpResponse
from .models import Country


def welcome(request):
    return render(request, 'welcome.html')


def get_all_countries(request):
    response = requests.get("https://restcountries.com/v3.1/all")

    for country_in_json in response.json():
        country = Country()
        country.from_json(country_in_json)

    return HttpResponse(response, content_type='application/json')
