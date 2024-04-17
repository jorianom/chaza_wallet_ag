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

# Queries for User_ms python


def getUser(id):
    response = requests.get(f"{urlUsers}{id}")
    if response.status_code == 200:
        data = response.json()
        # result = response.json()

        # print(result[1]["id"])
        return User(
            id=data.get('id'),  # .get evita errores por campo no existente
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            role=data.get('role'),
            date_birth=data.get('date_birth'),
            phone=data.get('phone'),
            document_type=data.get('document_type'),
            document_number=data.get('document_number')
        )
    else:
        return None


def getUsers():
    response = requests.get(f"{urlUsers}")
    if response.status_code == 200:
        result = response.json()
        return [User(
            id=data.get('id'),  # .get evita errores por campo no existente
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            role=data.get('role'),
            date_birth=data.get('date_birth'),
            phone=data.get('phone'),
            document_type=data.get('document_type'),
            document_number=data.get('document_number')
        )for data in result]
    else:
        return None

# Queries for transactions_ms TypeScript


def getTransactionsResolve():
    response = requests.get(f"{urlTransactions}/transactions")
    if response.status_code == 200:
        return response.json()
    else:
        return None


def getTransactionsForUserResolve(id):
    response = requests.get(f"{urlTransactions}/transactions/{id}")
    if response.status_code == 200:
        return response.json()
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
    response = graphene.Field(Response)

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
        response = Response(
            message="Recarga en proceso ..."
        )
        return CreateRecharge(ok=True, response=response)
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


class CreateMethod(graphene.Mutation):
    class Arguments:
        user = graphene.String(required=True)
        name = graphene.String(required=True)
        titular = graphene.String(required=True)
        duedate = graphene.String(required=True)
        number = graphene.String(required=True)
        type = graphene.String(required=True)
        sucursal = graphene.String(required=True)
    ok = graphene.Boolean()
    response = graphene.Field(MethodResponse)

    def mutate(self, info,  user, name, titular, duedate, number, type, sucursal):
        route = "method"
        data = {
            'user': user,
            'name': name,
            'titular': titular,
            'duedate': duedate,
            'number': number,
            'type': type,
            'sucursal': sucursal
        }
        url = f"{urlGolang}{route}"
        response = requests.post(url, json=data)
        if response.status_code == 200:
            json = response.json()
            response = MethodResponse(
                id=json['id'],
                status=json['status']
            )
            return CreateMethod(ok=True, response=response)
        else:
            raise GraphQLError('Hubo un error al realizar la petición')


class DeleteMethod(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
    ok = graphene.Boolean()
    response = graphene.Field(Response)

    def mutate(self, info, id):
        route = "method/"+id

        url = f"{urlGolang}{route}"
        response = requests.delete(url)
        if response.status_code == 200:
            data = response.json()
            print(response.json())
            response = Response(
                message=data['message'],
                status=data['status']
            )
            return DeleteMethod(ok=True, response=response)
        else:
            raise GraphQLError('Hubo un error al realizar la petición')


class UpdateMethod(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
        user = graphene.String(required=True)
        name = graphene.String(required=True)
        titular = graphene.String(required=True)
        duedate = graphene.String(required=True)
        number = graphene.String(required=True)
        type = graphene.String(required=True)
        sucursal = graphene.String(required=True)
    ok = graphene.Boolean()
    response = graphene.Field(Response)

    def mutate(self, info, id, user, name, titular, duedate, number, type, sucursal):
        route = "method/"+id
        data = {
            'user': user,
            'name': name,
            'titular': titular,
            'duedate': duedate,
            'number': number,
            'type': type,
            'sucursal': sucursal
        }
        url = f"{urlGolang}{route}"
        response = requests.put(url, json=data)
        if response.status_code == 200:
            json = response.json()
            response = Response(
                message=json['message'],
                status=json['status']
            )
            return UpdateMethod(ok=True, response=response)
        else:
            raise GraphQLError('Hubo un error al realizar la petición')
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
        elif response.status_code == 401:
            raise GraphQLError('Usuario o contraseña incorrectos')
        else:
            raise GraphQLError('Hubo un error al realizar la petición')

# Mutations users_ms
# CreateUser


class CreateUser(graphene.Mutation):
    class Arguments:

        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        date_birth = graphene.String(required=True)
        role = graphene.String(required=True)
        phone = graphene.String(required=True)
        document_type = graphene.String(required=True)
        document_number = graphene.String(required=True)
    ok = graphene.Boolean()
    user = graphene.Field(User)

    def mutate(self, info, first_name, last_name, date_birth, role, phone, document_type, document_number):
        data = {
            'first_name': first_name,
            'last_name': last_name,
            'role': role,
            'date_birth': date_birth,
            'phone': phone,
            'document_type': document_type,
            'document_number': document_number
        }

        url = f"{urlUsers}"
        response = requests.post(url, json=data)

        if response.status_code == 201:
            user = User(
                first_name,
                last_name,
                role,
                date_birth,
                phone,
                document_type,
                document_number
            )
            return CreateUser(ok=True, user=user)
        else:
            raise GraphQLError('Hubo un error al realizar la petición')

# Update user credentials


class UpdateUser(graphene.Mutation):
    class Arguments:
        # id = graphene.String(required=True)
        id = graphene.ID(required=True)
        userProperty = graphene.String(required=True)

    ok = graphene.Boolean()
    user = graphene.Field(User)

    def mutate(self, info, id, userProperty):
        data = {
            'phone': userProperty
        }

        url = f"{urlUsers}{id}"
        response = requests.put(url, json=data)

        if response.status_code == 200:
            user = response.json()
            return UpdateUser(ok=True, user=user)
        else:
            raise GraphQLError('Hubo un error al realizar la petición')

# Delete user credentials


class DeleteUser(graphene.Mutation):
    class Arguments:
        # id = graphene.String(required=True)
        id = graphene.ID(required=True)

    ok = graphene.Boolean()

    def mutate(self, info, id):

        url = f"{urlUsers}{id}"
        response = requests.delete(url)

        if response.status_code == 204:
            return DeleteUser(ok=True)
        else:
            raise GraphQLError('Hubo un error al realizar la petición')

# Queries Products_ms


def getProduct(id):
    route = "Product/"
    response = requests.get(f"{urlProducts}{route}{id}")
    if response.status_code == 200:
        data = response.json()
        # print(result)
        # print(result[1]["id"])
        return Product(
            id=data.get('id'),  # .get evita errores por campo no existente
            userID=data.get('userID'),
            kind=data.get('kind'),
            ea=data.get('ea'),
            amount=data.get('amount'),
            installments=data.get('installments'),
            dateTime=data.get('dateTime')
        )
    else:
        return None

# Mutations Products_ms
# Create Product


class CreateProduct(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        userID = graphene.String(required=True)
        kind = graphene.String(required=True)
        ea = graphene.String(required=True)
        amount = graphene.Int(required=True)
        installments = graphene.Int(required=True)
        dateTime = graphene.String(required=True)
    ok = graphene.Boolean()
    product = graphene.Field(Product)

    def mutate(self, info, id, userID, kind, ea, amount, installments, dateTime):
        route = "Product"
        data = {
            "id": id,
            "userID": userID,
            "kind": kind,
            "ea": ea,
            "amount": amount,
            "installments": installments,
            "dateTime": dateTime,
        }

        url = f"{urlProducts}{route}"
        response = requests.post(url, json=data)

        if response.status_code == 200:
            product = Product(
                id,
                userID,
                kind,
                ea,
                amount,
                installments,
                dateTime
            )
            return CreateProduct(ok=True, product=product)
        else:
            raise GraphQLError('Hubo un error al realizar la petición')

# Update Product


class UpdateProduct(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        userID = graphene.String(required=True)
        kind = graphene.String(required=True)
        ea = graphene.String(required=True)
        amount = graphene.Int(required=True)
        installments = graphene.Int(required=True)
        dateTime = graphene.String(required=True)

    ok = graphene.Boolean()
    product = graphene.Field(Product)

    def mutate(self, info, id, userID, kind, ea, amount, installments, dateTime):
        route = "Product"
        data = {
            "id": id,
            "userID": userID,
            "kind": kind,
            "ea": ea,
            "amount": amount,
            "installments": installments,
            "dateTime": dateTime,
        }

        url = f"{urlProducts}{route}"
        response = requests.put(url, json=data)

        product = response.json()
        print(product)
        if response.status_code == 200:
            product = response.json()
            return UpdateProduct(ok=True, product=product)
        else:
            raise GraphQLError('Hubo un error al realizar la petición')

# Delete Product


class DeleteProduct(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    ok = graphene.Boolean()

    def mutate(self, info, id):

        route = "Product/"
        url = f"{urlProducts}{route}{id}"
        response = requests.delete(url)

        if response.status_code == 200:
            return DeleteProduct(ok=True)
        else:
            raise GraphQLError('Hubo un error al realizar la petición')

# Mutations for transactions_ms TypeScript


class AddTransaction(graphene.Mutation):
    class Arguments:
        amount = graphene.Float(required=True)
        dateTime = graphene.String(required=True)
        description = graphene.String(required=True)
        senderId = graphene.Int(required=True)
        receiverId = graphene.Int(required=True)

    transactionId = graphene.Int()

    def mutate(self, info, amount, dateTime, description, senderId, receiverId):
        response = requests.post(
            f"{urlTransactions}/transactions",
            json={
                "amount": amount,
                "dateTime": dateTime,
                "description": description,
                "senderId": senderId,
                "receiverId": receiverId
            }
        )
        if response.status_code == 200:
            return AddTransaction(transactionId=response.json().get('transactionId'))
        else:
            raise GraphQLError('Failed to add transaction')
