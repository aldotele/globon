from django.urls import path
from country.views import get_all_countries

urlpatterns = [
    path('all', get_all_countries, name='get_all_countries'),
]