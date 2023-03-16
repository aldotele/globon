from django.urls import path
from world_proxy.views import welcome, get_all_countries

urlpatterns = [
    path('', welcome, name='welcome'),
    path('countries/all', get_all_countries, name='get_all_countries')
]