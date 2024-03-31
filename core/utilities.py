import json
import graphene
from graphql import GraphQLError
from core.producer import Producer
import requests

from core.typeDefs import *

# Queries Microserver Golang
def getRechargesResolve(id):
    route = "recharges/"
    response = requests.get(f"{urlGolang}{route}{id}")
    if response.status_code == 200:
        result = response.json().get("data")
        # print(result[1]["id"])
        return [Recharge(
            id=data.get('id'),  # .get evita errores por campo no existente
            user=data.get('user'),
            amount=data.get('amount'),
            method=data.get('method'),
            date=data.get('date'),
            status=data.get('status')
        )for data in result]
    else:
        return None

def getMethodsResolve(id):
    route = "methods/"
    response = requests.get(f"{urlGolang}{route}{id}")
    if response.status_code == 200:
        result = response.json().get("data")
        return [Method(
            id=data.get('id'),  # .get evita errores por campo no existente
            user=data.get('user'),
            name=data.get('name'),
            titular=data.get('titular'),
            duedate=data.get('duedate'),
            number=data.get('number'),
            type=data.get('type'),
            sucursal=data.get('sucursal')
        )for data in result]
    else:
        return None

# Mutations Microserver Golang
class CreateRecharge(graphene.Mutation):
    class Arguments:
        # id = graphene.String(required=True)
        user = graphene.String(required=True)
        amount = graphene.String(required=True)
        method = graphene.String(required=True)
        date = graphene.String(required=True)
        status = graphene.String()
    ok = graphene.Boolean()
    recharge = graphene.Field(Recharge)

    def mutate(self, info, user, amount, method, date):
        route = "recharge"
        producer = Producer()
        producer.connect("recharges")
        data = {
            'user': user,
            'amount': amount,
            'method': method,
            'date': date,
            'status': 'pending'
        }

        request_json = json.dumps(data)
        url = f"{urlGolang}{route}"
        producer.publish(request_json)
        # response = requests.post(url, json=data)
        # if response.status_code == 200:
        #     data = response.json().get("recharge")

        #     recharge = Recharge(
        #         id=data['id'],
        #         user=data['user'],
        #         amount=data['amount'],
        #         method=data['method'],
        #         date=data['date'],
        #         status=data['status']
        #     )
        #     return CreateRecharge(ok=True, recharge=recharge)
        # else:
        #     raise GraphQLError('Hubo un error al realizar la petición')

# Mutations auth_ms Java Spring
# Register user credentials
class CreateUserAuth(graphene.Mutation):
    class Arguments:
        # id = graphene.String(required=True)
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    ok = graphene.Boolean()
    userAuth = graphene.Field(UserAuth)

    def mutate(self, info, username, password):
        data = {
            'username': username,
            'password': password
        }

        route = "register"
        url = f"{urlAuth}{route}"
        response = requests.post(url, json=data)

        if response.status_code == 200:
            userAuth = UserAuth(
                username,
                password
            )
            return CreateUserAuth(ok=True, userAuth=userAuth)
        else:
            raise GraphQLError('Hubo un error al realizar la petición')

# Update user credentials
class UpdateUserAuth(graphene.Mutation):
    class Arguments:
        # id = graphene.String(required=True)
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    ok = graphene.Boolean()
    userAuth = graphene.Field(UserAuth)

    def mutate(self, info, username, password):
        data = {
            'username': username,
            'password': password
        }

        route = "update/"
        url = f"{urlAuth}{route}{username}"
        response = requests.put(url, json=data)

        if response.status_code == 200:
            userAuth = UserAuth(
                username,
                password
            )
            return UpdateUserAuth(ok=True, userAuth=userAuth)
        else:
            raise GraphQLError('Hubo un error al realizar la petición')

# Delete user credentials
class DeleteUserAuth(graphene.Mutation):
    class Arguments:
        # id = graphene.String(required=True)
        username = graphene.String(required=True)

    ok = graphene.Boolean()

    def mutate(self, info, username):

        route = "delete/"
        url = f"{urlAuth}{route}{username}"
        response = requests.delete(url)

        if response.status_code == 200:
            return DeleteUserAuth(ok=True)
        else:
            raise GraphQLError('Hubo un error al realizar la petición')

# Authenticate user credentials
class AuthenticateUserAuth(graphene.Mutation):
    class Arguments:
        # id = graphene.String(required=True)
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    ok = graphene.Boolean()
    token = graphene.String()

    def mutate(self, info, username, password):
        data = {
            'username': username,
            'password': password
        }

        route = "authenticate"
        url = f"{urlAuth}{route}"
        response = requests.post(url, json=data)

        if response.status_code == 200:
            token = response.json().get("accessToken")
            return AuthenticateUserAuth(ok=True, token=token)
        else:
            raise GraphQLError('Hubo un error al realizar la petición')