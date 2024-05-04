import graphene
import os
from dotenv import load_dotenv
load_dotenv()
''' 
# Example
class Char(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()
    status = graphene.String()
    species = graphene.String()
'''

# Microserver Golang
# "https://go-recharges-ms-yerq2evawq-uc.a.run.app/api/" #"http://localhost:5000/api/"
urlGolang = os.getenv('URL_GOLANG')


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


class Response(graphene.ObjectType):
    message = graphene.String()
    status = graphene.String()
    data = graphene.ObjectType()


class MethodResponse(graphene.ObjectType):
    id = graphene.ID()
    status = graphene.Int()
    recharge = graphene.ObjectType()


# auth_ms Java Spring
urlAuth = "http://localhost:8080/auth/"


class UserAuth(graphene.ObjectType):
    username = graphene.String()
    password = graphene.String()


# users_ms python
urlUsers = "http://localhost:4000/UsersUN/"


class User(graphene.ObjectType):
    id = graphene.ID()
    first_name = graphene.String()
    last_name = graphene.String()
    role = graphene.String()
    date_birth = graphene.String()
    phone = graphene.String()
    document_type = graphene.String()
    document_number = graphene.String()


# products_ms c#
urlProducts = "http://localhost:3030/api/"


class Product(graphene.ObjectType):
    id = graphene.ID()
    userID = graphene.String()
    kind = graphene.String()
    ea = graphene.String()
    amount = graphene.String()
    installments = graphene.String()
    dateTime = graphene.String()


# transactions_ms TypeScript
urlTransactions = "http://localhost:3003"


class Transaction(graphene.ObjectType):
    transactionId = graphene.Int()
    amount = graphene.Float()
    dateTime = graphene.String()
    description = graphene.String()
    senderId = graphene.Int()
    receiverId = graphene.Int()
    senderPhone = graphene.String()
    receiverPhone = graphene.String()
