from django.shortcuts import render
import requests
from django.http import HttpResponse
import json


def welcome(request):
    return render(request, 'welcome.html')


def get_all_countries(request):
    response = requests.get("https://restcountries.com/v3.1/all")
    body = json.loads(response.content)

    print(body[0]["name"]["common"])
    return HttpResponse(response, content_type='application/json')
