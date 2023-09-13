from django_filters import rest_framework

from .models import City


class CityFilters(rest_framework.FilterSet):
    iso2 = rest_framework.CharFilter(
        field_name="iso2",
        lookup_expr="exact"
    )

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

    class Meta:
        model = City
        fields = ["maxPopulation", "minPopulation", "iso2", "iso3"]