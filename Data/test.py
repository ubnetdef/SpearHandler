# from graphene import ObjectType, String, Schema

# class Query(ObjectType):
#     # this defines a Field `hello` in our Schema with a single Argument `first_name`
#     # By default, the argument name will automatically be camel-based into firstName in the generated schema
#     hello = String(first_name=String(default_value="stranger"))
#     goodbye = String()

#     # our Resolver method takes the GraphQL context (root, info) as well as
#     # Argument (first_name) for the Field and returns data for the query Response
#     def resolve_hello(root, info, first_name):
#         return f'Hello {first_name}!'

#     def resolve_goodbye(root, info):
#         return 'See ya!'

# schema = Schema(query=Query)

from graphene import relay, ObjectType, String, Schema, List
import graphene

class Service(relay.ClientIDMutation):
    name = graphene.String()
    port = graphene.Int()
    externalAccessibility = graphene.Boolean()

    def resolve_name(root, info):
        return f'{root.name}'
    
    @classmethod
    def mutate_and_get_payload():
        name = "test"

schema = Schema(query=Service)

query_string = '{ name }'
result = schema.execute(query_string)
print(result.data)