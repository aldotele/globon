from django_filters import rest_framework
from rest_framework import filters

from .models import City


class CustomCapitalFilter(rest_framework.BooleanFilter):
    def filter(self, qs, value):
        if value:
            return qs.filter(**{self.field_name + '__in': ["primary"]})
        return qs


class CustomCountyCapitalFilter(rest_framework.BooleanFilter):
    def filter(self, qs, value):
        if value:
            return qs.filter(**{self.field_name + '__in': ["primary", "admin", "minor"]})
        # TODO when value is false it gets here as None (same as when not selected
        # need to handle
        return qs


class CityFilters(rest_framework.FilterSet):

    iso3 = rest_framework.CharFilter(
        field_name="iso3",
        lookup_expr="exact"
    )

    maxPopulation = rest_framework.NumberFilter(
        field_name="population",
        lookup_expr="lte"
    )

    minPopulation = rest_framework.NumberFilter(
        field_name="population",
        lookup_expr="gte"
    )

    #capital = CustomCapitalFilter(field_name="capital")

    #countyCapital = CustomCountyCapitalFilter(field_name="capital")


    class Meta:
        model = City
        fields = ["maxPopulation", "minPopulation", "iso3", "capital"]
