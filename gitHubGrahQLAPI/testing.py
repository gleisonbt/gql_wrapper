import json
import requests
import random

token = '773e67ef75e7274d5eef5722b1e714cc6c6770cc' #gleison

URL = 'https://api.github.com' 

def restCall(query, token=token):
    r = requests.get(query, headers={'Authorization': 'Bearer '+ token})
    return r.json()

endpoints = [
    {
        'path':'/users/{username:string}/repos',
        'parameters':[{'type':'string'},{'sort':'string'},{'direction':'string'}],
        'example':'https://api.github.com/users/gleisonbt/repos'
    }
    # ,
    # {
    #     'path':'/users/{username:string}/starred',
    #     'parameters':[{'type':'string'},{'sort':'string'},{'direction':'string'}],
    #     'example':'https://api.github.com/users/gleisonbt/starred'
    # }
    ,
    {
        'path':'/users',
        'parameters':[{'since':'int'},{'per_page':'int'}, {'page':'int'}],
        'example':'https://api.github.com/users?since=125'
    }
]


def path_variables(endpoint):
    path_variables = []
    paths  = endpoint['path'].split('/')
    for path in paths[1:len(paths)]:
        if path[0] == '{':
            path_variables.append(path)
    return path_variables

def name_root_node(endpoint):
    paths = endpoint['path'].split('/')
    parameters = path_variables(endpoint)
    for path_variable in parameters:
        paths.remove(path_variable)
    del paths[0]
    
    cont = 1
    for path in paths[1:len(paths)]:
        paths[cont] = path[0].upper() + path[1:len(path)]
        cont = cont + 1

    name_root_name = ''
    for path in paths:
        name_root_name = name_root_name + path
    
    return name_root_name


def parseTypes(key, value):
    type_class = type(value)

    if type_class == str:
        return 'String'
    elif type_class == int:
        return 'Int'
    elif str(type_class.__name__) == 'NoneType':
        return 'String'
    elif type_class == bool:
        return 'Boolean'
    elif type_class == float:
        return 'Float'
    elif type_class == dict:
        rootType =  key[0].upper() + key[1:len(key)]
        if rootType in type_list:
            return rootType + "_" + str(type_list.count(rootType))
        return rootType
    elif type_class == list:
        return '[' + parseTypes(key, value[0]) + ']'

type_list = []


def json2graphql(json, rootType):

    schema = ""
    if type(json) == list:
        data = json[0]
    else:
        data = json
     
    if rootType in type_list:
        rootType = rootType + '_' + str(type_list.count(rootType))

    schema = schema + "type " + rootType + " {" + "\n"
    
    for key in data.keys():

        schema = schema + '\t' + key + ": " + parseTypes(key, data[key]) + '\n'
        if type(data[key]) == dict:
            schema = json2graphql(data[key], parseTypes(key, data[key])) + schema

    schema = schema + '}' + '\n'

    type_list.append(rootType)
    
    return schema
   

def convert_types(path_type):
    if path_type == 'string':
        return 'String'
    elif path_type == 'int':
        return 'Int'
    elif path_type == 'float':
        return 'Float'
    elif path_type == 'bool':
        return 'Boolean'
    elif path_type == 'id':
        return 'ID'
    else:
        return 'String'

def generate_query(endpoints):
    query_type = "type Query {\n"
    for endpoint in endpoints:
        query_name = name_root_node(endpoint)

        query_type = query_type + '\t' + query_name + '(' 

        parameters = path_variables(endpoint)

        for parameter in parameters:
            parameter = parameter.replace('{', '')
            parameter = parameter.replace('}', '')
            var_name, type_name = parameter.split(':')
            query_type = query_type + var_name + ':' + convert_types(type_name) + ", "
        
        for parameter in endpoint['parameters']:
            var_name = list(parameter.keys())[0]
            type_name = convert_types(parameter[list(parameter.keys())[0]])
            query_type = query_type + var_name + ':' + type_name + ", "

        if type(restCall(endpoint['example'])) is list:
            query_type = query_type + '):' + '[' + name_root_node(endpoint) + ']' + '\n'
        else:
            query_type = query_type + '):' + name_root_node(endpoint) + '\n'          
        # + var_name + ':' + ')'
        

    query_type = query_type +  "}"


    return query_type

def generate_schema(endpoints):
    schema = ""
    for endpoint in endpoints:
        data = restCall(endpoint['example'])
        root_node = name_root_node(endpoint)
        schema = schema + json2graphql(data, root_node)
    
    schema = schema + generate_query(endpoints)

    schema = schema + """
schema {
    query: Query
}"""

    return schema

schema = generate_schema(endpoints)

f = open("schema.graphql", "w")
f.write(schema)