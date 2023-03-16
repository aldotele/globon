from django.shortcuts import render
import requests
from django.http import HttpResponse

def welcome(request):
    return render(request, 'welcome.html')

def get_all_countries(request):
    response = requests.get("https://restcountries.com/v3.1/all")
    return HttpResponse(response, content_type='application/json')
