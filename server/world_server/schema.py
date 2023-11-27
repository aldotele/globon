import graphene

import country.schema


class Query(country.schema.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
