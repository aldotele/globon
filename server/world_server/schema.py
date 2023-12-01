import graphene

import country.schema
import city.schema


class Query(country.schema.Query, city.schema.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
