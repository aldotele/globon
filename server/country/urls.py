from django.urls import path

from country.views import CountryList, CountryGeographyList, CountryEconomyList, CountrySocietyList, CountryFieldList, \
    CountryGeographyFieldList, CountryEconomyFieldList, CountrySocietyFieldList

urlpatterns = [
    path('', CountryList.as_view()),
    path('geography', CountryGeographyList.as_view()),
    path('society', CountrySocietyList.as_view()),
    path('economy', CountryEconomyList.as_view()),
    # APIs to retrieve fields
    path('fields', CountryFieldList.as_view()),
    path('geography/fields', CountryGeographyFieldList.as_view()),
    path('society/fields', CountrySocietyFieldList.as_view()),
    path('economy/fields', CountryEconomyFieldList.as_view()),
]

