import graphene
from graphene_django import DjangoObjectType, filter #used to change Django object into a format that is readable by GraphQL
from country.models import Country
import django_filters

# class CountryFilter(django_filters.FilterSet):
#     population = django_filters.RangeFilter()

#     class Meta:
#         model = Country
#         fields = ("population",)

class CountryNode(DjangoObjectType):
    class Meta:
        model = Country
        filter_fields = {
            'name' : ['exact', 'istartswith'],
            'population' : ['range'],
            'income_level': ['exact']
        }
        interfaces = (graphene.relay.Node, )

class CountryType(DjangoObjectType):
    # Describe the data that is to be formatted into GraphQL fields
    class Meta:
        model = Country
        #filterset_class = CountryFilter
        field = ("uuid", "name", "official_name",
                 "iso_code", "population", "flag",
                 "capital", "translations", "currencies",
                 "map", "languages", "borders", "income_level")
        # filterset_fields = {
        #     'population': ['range']
        # }
        # interfaces = (graphene.relay.Node,)

class Query(graphene.ObjectType):
    #query CountryType to get list of countries
    country = graphene.relay.Node.Field(CountryNode)
    all_countries = filter.DjangoFilterConnectionField(CountryNode)
    list_country=graphene.List(CountryType)
    read_country=graphene.Field(CountryType, iso_code=graphene.String())
    #list_countries_by_population_range=filter.DjangoFilterConnectionField(CountryType)

    def resolve_list_country(root, info):
        # We can easily optimize query count in the resolve method
        return Country.objects.all()
    
    def resolve_read_country(root, info, iso_code):
        # get data where iso code in the database = iso code queried from the frontend
        return Country.objects.get(iso_code=iso_code)
    
    #def resolve_list_countries_by_population_range(root, info, minPop, maxPop):
    #    return Country.objects.filter(population__gte=maxPop, population__lte=minPop)
  
schema = graphene.Schema(query=Query)