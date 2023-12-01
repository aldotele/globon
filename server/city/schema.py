import graphene
from graphene_django import DjangoObjectType

from country.util.filter_utils import extract_field_value
from city.models import City
from graphql import GraphQLError


class CityType(DjangoObjectType):
    class Meta:
        model = City


class Query(graphene.ObjectType):
    cities = graphene.List(CityType, search=graphene.String())

    def resolve_cities(self, info, search=""):
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
            queryset = City.objects.filter(**filter_dict)
            if len(queryset) > 300:
                return GraphQLError("too many results: please restrict your search criteria")
            return queryset
        else:
            return GraphQLError("error: please apply search criteria")


schema = graphene.Schema(query=Query)
