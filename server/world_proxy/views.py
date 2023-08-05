from django.shortcuts import render
from django.http import JsonResponse


def welcome(request):
    return render(request, 'welcome.html')


def ready(request):
    return JsonResponse({'ready': True})
