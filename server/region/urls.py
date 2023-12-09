from django.urls import path

from .views import CountryRegionsList

urlpatterns = [
    # can be iso3 or iso3
    path('<str:iso>', CountryRegionsList.as_view()),
]
