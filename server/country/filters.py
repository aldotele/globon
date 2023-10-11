from django_filters import rest_framework

from country.models import Country


class CountryFilters(rest_framework.FilterSet):
    incomeLevel = rest_framework.CharFilter(
        field_name="income_level",
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

    language = rest_framework.CharFilter(
        field_name="languages",
        lookup_expr="icontains"
    )

    isoCode = rest_framework.CharFilter(
        field_name="iso3",
        lookup_expr="iexact"
    )

    class Meta:
        model = Country
        fields = ["maxPopulation", "minPopulation", "incomeLevel", "language", "iso3"]
