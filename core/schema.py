import graphene
import requests

from core.typeDefs import Char



class Query(graphene.ObjectType):
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


schema = graphene.Schema(query=Query)
