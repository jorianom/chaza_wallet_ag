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

    # Users python

    getUser = graphene.Field(User,id=graphene.ID())
    getUsers = graphene.List(User)

    def resolve_getUser(self,info,id):
        return getUser(id)
    
    def resolve_getUsers(self,info):
        return getUsers()
    

    # Products c#
    
    getProduct = graphene.Field(Product,id=graphene.ID())
    
    def resolve_getProduct(self, info, id):
        return getProduct(id)

    # Transactions
    getTransactions = graphene.List(Transaction)

    def resolve_getTransactions(self, info):
        return getTransactionsResolve()
    
    getTransactionsForUser = graphene.List(Transaction, id=graphene.Int())

    def resolve_getTransactionsForUser(self, info, id):
        return getTransactionsForUserResolve(id)


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

    # users_ms python Django

    postUsers = CreateUser.Field()
    updateUser = UpdateUser.Field()
    deleteUser = DeleteUser.Field()
    
    # products_ms c# firebase
    
    postProduct = CreateProduct.Field()
    updateProduct = UpdateProduct.Field()
    deleteProduct = DeleteProduct.Field()
    

    # transactions_ms TypeScript
    addTransaction = AddTransaction.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)