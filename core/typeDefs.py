import graphene
import os
import jwt
from graphql import GraphQLError
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
# os.getenv('URL_GOLANG')
# "https://go-recharges-ms-yerq2evawq-uc.a.run.app/api/"
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

secret = "G6qmQ3F1EIjaoafKpnw6wFvaK69MzoZVVIhk4Ex5qqSRO7fVAxnzpXW7FOi9tRIKhqFunQyMZjeuZRFxbJegGg=="

def validate_authorization(info, secret):
    # Extraer request
    request = info.context
        
    # Extraer authorization header
    authorization_header = request.headers.get('Authorization')
    if not authorization_header:
        raise GraphQLError('Error: header de autorización no fue suministrado')
    
    # Extraer token
    parts = authorization_header.split()
    if len(parts) != 2 or parts[0].lower() != 'bearer':
        raise GraphQLError('Error: formato de header de autorización inválido')
    token = parts[1]
    
    # DEBUG
    print("JWT: ", token)

    # Validar token
    try:
        decoded_payload = jwt.decode(token, secret, algorithms=['HS512'])
    except jwt.ExpiredSignatureError:
        raise GraphQLError('Error: el token ha expirado')
    except jwt.InvalidTokenError:
        raise GraphQLError("Error: el token es inválido")

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
