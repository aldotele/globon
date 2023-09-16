from django_filters import rest_framework

from .models import City


class CustomCapitalFilter(rest_framework.BooleanFilter):
    def filter(self, qs, value):
        if value is None:
            return qs
        elif value:
            return qs.filter(**{self.field_name + '__in': ["primary"]})
        else:
            return qs.filter(**{self.field_name + '__in': ["", "admin", "minor"]})


class CustomCountyCapitalFilter(rest_framework.BooleanFilter):
    def filter(self, qs, value):
        if value is None:
            return qs
        elif value:
            return qs.filter(**{self.field_name + '__in': ["primary", "admin", "minor"]})
        else:
            return qs.filter(**{self.field_name + '__in': [""]})


class CityFilters(rest_framework.FilterSet):

    iso3 = rest_framework.CharFilter(
        field_name="iso3",
        lookup_expr="exact"
    )

    smId = rest_framework.NumberFilter(
        field_name="sm_id",
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

    capital = CustomCapitalFilter(field_name="capital")

    countyCapital = CustomCountyCapitalFilter(field_name="capital")

    class Meta:
        model = City
        fields = ["maxPopulation", "minPopulation", "iso3", "smId", "capital", "countyCapital"]
