import graphene
from graphene_django import DjangoObjectType

from country.util.filter_utils import extract_field_value
from .models import Country, CountryGeography, CountrySociety, CountryEconomy


class CountryGeographyType(DjangoObjectType):
    class Meta:
        model = CountryGeography
        fields = "__all__"


class CountrySocietyType(DjangoObjectType):
    class Meta:
        model = CountrySociety
        fields = "__all__"


class CountryEconomyType(DjangoObjectType):
    class Meta:
        model = CountryEconomy
        fields = "__all__"


class CountryType(DjangoObjectType):
    class Meta:
        model = Country
        fields = "__all__"


class Query(graphene.ObjectType):
    countries = graphene.List(CountryType, search=graphene.String())

    def resolve_countries(self, info, search=""):
        if search:
            filter_dict = {}
            for filter in search.split("&"):
                filter = filter.strip().lower()
                if "=" in filter:
                    field_name, value = extract_field_value(filter, "=")
                    field_name_iexact = field_name + "__iexact"
                    filter_dict[field_name_iexact] = value
                if ">" in filter:
                    field_name, value = extract_field_value(filter, ">")
                    field_name_gt = field_name + "__gt"
                    filter_dict[field_name_gt] = value
                if "<" in filter:
                    field_name, value = extract_field_value(filter, "<")
                    field_name_lt = field_name + "__lt"
                    filter_dict[field_name_lt] = value
                if "contains" in filter:
                    field_name, value = extract_field_value(filter, "contains")
                    field_name_icontains = field_name + "__icontains"
                    filter_dict[field_name_icontains] = value

            return Country.objects.filter(**filter_dict)

        else:
            return Country.objects.all()


schema = graphene.Schema(query=Query)
