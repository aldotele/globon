import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError

from city.models import City
from util.exception.filter_exception import FilterException
from util.filter import build_application_filter


class CityType(DjangoObjectType):
    class Meta:
        model = City
        fields = "__all__"


class Query(graphene.ObjectType):
    cities = graphene.List(CityType, search=graphene.String())

    def resolve_cities(self, info, search=""):
        if search:
            try:
                filter_dict = build_application_filter(search, City.get_fields())
            except FilterException as e:
                return GraphQLError(str(e))
            queryset = City.objects.filter(**filter_dict)
            if len(queryset) > 300:
                return GraphQLError("too many results: please restrict your search criteria")
            return queryset
        else:
            return GraphQLError("error: please apply search criteria")


schema = graphene.Schema(query=Query)
