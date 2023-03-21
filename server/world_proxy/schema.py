import graphene
from graphene_django import DjangoObjectType
from .models import Country

class CountryType(DjangoObjectType):
    class Meta: 
        model = Country
        fields = ('name','official_name', 'acronym', 'capital', 'population')

class Query(graphene.ObjectType):
    countires = graphene.List(CountryType)

    def resolve_countries(root, info, **kwargs):
        # Querying a list
        return Country.objects.all()

schema = graphene.Schema(query=Query)