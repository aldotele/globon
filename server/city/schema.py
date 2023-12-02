import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError

from city.models import City
from util.filter import build_application_filter


class CityType(DjangoObjectType):
    class Meta:
        model = City


class Query(graphene.ObjectType):
    cities = graphene.List(CityType, search=graphene.String())

    def resolve_cities(self, info, search=""):
        if search:
            filter_dict = build_application_filter(search)
            queryset = City.objects.filter(**filter_dict)
            if len(queryset) > 300:
                return GraphQLError("too many results: please restrict your search criteria")
            return queryset
        else:
            return GraphQLError("error: please apply search criteria")


schema = graphene.Schema(query=Query)
