from django.urls import path
from country.views import CountryList

urlpatterns = [
    path('', CountryList.as_view()),
]

