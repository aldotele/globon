from django.http import HttpResponse
from django.shortcuts import render
import requests
from country.models import Country

def welcome(request):
    return render(request, 'welcome.html')

def populate_db_with_countries(request):
    response = requests.get("https://restcountries.com/v3.1/all")
    for country_in_json in response.json():
        country = Country()
        country.from_json(country_in_json)
        country.save()
    return HttpResponse("done")
