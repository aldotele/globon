import graphene
from graphene_django import DjangoObjectType

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
    countries = graphene.List(CountryType)
    # country_geographies = graphene.List(CountryGeographyType)

    def resolve_countries(self, info):
        return Country.objects.all()

    """
    def resolve_country_geographies(self, info):
        return CountryGeography.objects.all()
    """


schema = graphene.Schema(query=Query)
