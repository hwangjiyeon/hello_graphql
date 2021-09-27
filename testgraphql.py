from graphene import ObjectType, String, Schema
import graphene
import json
from datetime import datetime

class User(graphene.ObjectType):
    id = graphene.ID()
    userName = graphene.String()
    lastLogin = graphene.DateTime(required=False)

class Query(ObjectType):
    hello =  graphene.List(User, first=graphene.Int())
    goodbye = String()

    def resolve_hello(self, info, first):
        return [
                   User(userName='Alice', lastLogin=datetime.now()),
                   User(userName='Bob', lastLogin=datetime.now()),
                   User(userName='Steven', lastLogin=datetime.now())
               ][:first]

    def resolve_goodbye(self, info):
        return 'Bye~'

def test_graphql():
    schema = Schema(query=Query)

    result = schema.execute('{ hello (first:1) { userName lastLogin} }')
    item = result.data['hello']
    print(json.dumps(item, indent=4))
    #print(result.data['hello'])


    result_goodbye = schema.execute('{ goodbye }')
    print(result_goodbye.data['goodbye'])
