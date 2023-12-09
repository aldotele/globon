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
        description = "Note that fields are in camelCase, " \
                      "but if you wish to use them inside the optional <search> parameter " \
                      "you must specify them in kebab_case: adminName --> admin_name"


class Query(graphene.ObjectType):
    cities = graphene.List(CityType,
                           search=graphene.String(description='the search filter must respect the following format: '
                                                              '"<field> <operator> <value>" '
                                                              'where <operator> can be one of [=, <, >, contains]. '
                                                              'For example one valid filter is: '
                                                              '"iso3 = ITA & population > 1000000". Note that you '
                                                              'can use multiple filters separated by &.'),
                           description= "query to retrieve cities, with an optional search parameter acting as a filter")

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
