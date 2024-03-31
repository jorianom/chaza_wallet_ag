import graphene
import requests

from core.typeDefs import *
from core.utilities import *

class Query(graphene.ObjectType):

    # Microserver Golang
    getRecharges = graphene.List(Recharge, id=graphene.ID())
    getMethods = graphene.List(Method, id=graphene.ID())

    def resolve_getRecharges(self, info, id):
        return getRechargesResolve(id)

    def resolve_getMethods(self, info, id):
        return getMethodsResolve(id)

    ''' # Examples
    hello = graphene.String(default_value="Hello W")
    external_data = graphene.Field(Char)
    external_data2 = graphene.List(Char, id=graphene.ID())

    def resolve_external_data2(self, info, id):
        response = requests.get(
            'https://rickandmortyapi.com/api/character/?page='+id)
        if response.status_code == 200:
            result = response.json().get("results")
            return [Char(
                id=data['id'],
                name=data['name'],
                status=data['status'],
                species=data['species'],
            )for data in result]
        else:
            return None

    def resolve_external_data(self, info):
        response = requests.get(
            'https://rickandmortyapi.com/api/character/2')
        if response.status_code == 200:
            data = response.json()

            return Char(
                id=data['id'],
                name=data['name'],
                status=data['status'],
                species=data['species'],
            )
        else:
            return None
'''

class Mutation(graphene.ObjectType):

    # Microserver Golang
    postRecharge = CreateRecharge.Field()

    # auth_ms Java Spring
    postUserAuth = CreateUserAuth.Field()
    updateUserAuth = UpdateUserAuth.Field()
    deleteUserAuth = DeleteUserAuth.Field()
    authenticateUserAuth = AuthenticateUserAuth.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)