import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError

from util.exception.filter_exception import FilterException
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
            try:
                filter_dict = build_application_filter(search, QueryHelper.fields)
            except FilterException as e:
                return GraphQLError(str(e))
            return Country.objects.filter(**filter_dict)

        else:
            return Country.objects.all()


class QueryHelper:
    fields = Country.get_fields() + \
             ["geography__" + field for field in CountryGeography.get_fields()] + \
             ["economy__" + field for field in CountryEconomy.get_fields()] + \
             ["society__" + field for field in CountrySociety.get_fields()]


schema = graphene.Schema(query=Query)
