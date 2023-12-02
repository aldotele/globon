import graphene
from graphene_django import DjangoObjectType

from util.filter import build_application_filter
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
            filter_dict = build_application_filter(search)
            return Country.objects.filter(**filter_dict)

        else:
            return Country.objects.all()


schema = graphene.Schema(query=Query)
