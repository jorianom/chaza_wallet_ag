import graphene
from graphql import GraphQLError
import requests

from core.typeDefs import Recharge, Method
from core.typeDefs import urlGolang

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
        data = {
            'user': user,
            'amount': amount,
            'method': method,
            'date': date,
            'status': 'pending'
        }

        url = f"{urlGolang}{route}"
        response = requests.post(url, json=data)
        if response.status_code == 200:
            data = response.json().get("recharge")

            recharge = Recharge(
                id=data['id'],
                user=data['user'],
                amount=data['amount'],
                method=data['method'],
                date=data['date'],
                status=data['status']
            )
            return CreateRecharge(ok=True, recharge=recharge)
        else:
            raise GraphQLError('Hubo un error al realizar la petición')
