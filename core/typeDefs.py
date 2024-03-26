import graphene

class Char(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()
    status = graphene.String()
    species = graphene.String()
