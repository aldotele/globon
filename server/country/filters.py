from django_filters import rest_framework

from country.models import Country, CountryGeography, CountryEconomy, CountrySociety


class CountryFilters(rest_framework.FilterSet):
    incomeLevel = rest_framework.CharFilter(
        field_name="income_level",
        lookup_expr="exact"
    )

    iso3 = rest_framework.CharFilter(
        field_name="iso3",
        lookup_expr="iexact"
    )

    iso2 = rest_framework.CharFilter(
        field_name="iso2",
        lookup_expr="iexact"
    )

    class Meta:
        model = Country
        fields = ["iso3", "iso2", "incomeLevel"]


class CountryGeographyFilters(rest_framework.FilterSet):

    iso3 = rest_framework.CharFilter(
        field_name="iso3",
        lookup_expr="iexact"
    )

    class Meta:
        model = CountryGeography
        fields = ["iso3"]


class CountryEconomyFilters(rest_framework.FilterSet):
    iso3 = rest_framework.CharFilter(
        field_name="iso3",
        lookup_expr="iexact"
    )

    class Meta:
        model = CountryEconomy
        fields = ["iso3"]


class CountrySocietyFilters(rest_framework.FilterSet):
    iso3 = rest_framework.CharFilter(
        field_name="iso3",
        lookup_expr="iexact"
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
        model = CountrySociety
        fields = ["iso3", "minPopulation", "maxPopulation"]