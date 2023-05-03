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

    class Meta:
        model = Country
        fields = ["population", "income_level"]