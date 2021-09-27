from graphene import ObjectType, String, Schema


class Query(ObjectType):
    hello = String(name=String(default_value='anonymous'))
    goodbye = String()

    def resolve_hello(self, info, name):
        return f'Hello {name}!'

    def resolve_goodbye(self, info):
        return 'Bye~'

def ex_graphql():
    schema = Schema(query=Query)

    result = schema.execute('{ hello }')
    print(result.data['hello'])
    # Hello anonymous!

    result_with_arg = schema.execute('{ hello(name: "jonnung") }')
    print(result_with_arg.data['hello'])
    # Hello jonnung!

    result_goodbye = schema.execute('{ goodbye }')
    print(result_goodbye.data['goodbye'])
