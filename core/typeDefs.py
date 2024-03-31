import graphene

''' 
# Example
class Char(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()
    status = graphene.String()
    species = graphene.String()
'''

# Microserver Golang
urlGolang = "http://localhost:3000/api/"

class Recharge(graphene.ObjectType):
    id = graphene.String()
    user = graphene.String()
    amount = graphene.String()
    method = graphene.String()
    date = graphene.String()
    status = graphene.String()

class Method(graphene.ObjectType):
    id = graphene.ID()
    user = graphene.String()
    name = graphene.String()
    titular = graphene.String()
    duedate = graphene.String()
    number = graphene.String()
    type = graphene.String()
    sucursal = graphene.String()

class RechargeResponse(graphene.ObjectType):
    id = graphene.ID()
    status = graphene.Int()
    recharge = graphene.ObjectType()

# auth_ms Java Spring
urlAuth = "http://host.docker.internal:8080/auth/"

class UserAuth(graphene.ObjectType):
    username = graphene.String()
    password = graphene.String()