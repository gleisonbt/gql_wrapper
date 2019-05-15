import json

endpoints = [
    {
        'path':'/users/{username:string}/repos',
        'parameters':[{'type':'string'},{'sort':'string'},{'direction':'string'}],
        'example':'https://api.github.com/users/gleisonbt/repos'
    },
    {
        'path':'/users/{username:string}/starred',
        'parameters':[{'type':'string'},{'sort':'string'},{'direction':'string'}],
        'example':'https://api.github.com/users/gleisonbt/starred'
    },
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



def generate_resolver(endpoint):
    function_name = name_root_node(endpoint)

    path_vars = []
    vars = []

    for path_variable in path_variables(endpoint):
        var_name = path_variable[1:len(path_variable) - 1].split(':')[0]
        path_vars.append(var_name)

    for parameter in endpoint['parameters']:
        var_name = list(parameter.keys())[0]
        vars.append(var_name)


    resolver_string = """def """

    params = str(path_vars + vars)[1:len(str(path_vars + vars))-1].replace('\'','')

    rest_call = "https://api.github.com" + endpoint['path'] 

    cont = 0
    for path_variable in path_variables(endpoint):
        rest_call = rest_call.replace(path_variable, "+ str(" + path_vars[cont] + ") +")
        cont = cont + 1

    if len(vars) > 0:
        rest_call = rest_call + "?" + vars[0] + "=" + " + str(" + vars[0] + ") + "
        for var in vars[1:len(vars) - 1]:
            rest_call = rest_call + "&" + var + "= + str(" + var + ") + "
        
        rest_call = rest_call + "&" + vars[len(vars) - 1] + "= + str(" + vars[len(vars) - 1] + ")"

    rest = ""

    for fragment in rest_call.split("+"):
        if not ("str(" in fragment):
            fragment = "+\'" + fragment + "\'+"
        
        rest = rest + fragment

    rest = rest[1:len(rest)] 


    resolver_string = resolver_string + " " + function_name + "(self, info, " + params + "):\n"
    resolver_string = resolver_string + "\t" + "entry = restCall(" + rest + ")\n"
    resolver_string = resolver_string + "\t" + "return json2obj(json.dumps(entry))"

    return resolver_string

def generate_connectors(endpoint):
    return "schema.get_query_type().fields[\'" + name_root_node(endpoint) + "\'].resolver = " + name_root_node(endpoint)



def code_generator(endpoints):
    code = """
import json
import os
from collections import namedtuple

from graphql import build_ast_schema
from graphql.language.parser import parse


import requests

token = '773e67ef75e7274d5eef5722b1e714cc6c6770cc' #gleison


def restCall(query, token=token):
    r = requests.get(query, headers={'Authorization': 'Bearer '+ token})
    print(r.status_code)
    return r.json()


def _json_object_hook(d):
    return namedtuple('X', d.keys())(*d.values())


def json2obj(data):
    return json.loads(data, object_hook=_json_object_hook)

def parse_schema(document):
    return build_ast_schema(parse(document))

f = open("schema.graphql", "r")

string = ""
while 1:
    line = f.readline()
    if not line:break
    string += line

f.close()


schema = parse_schema(string)

f.close()
    """
    for endpoint in endpoints:
        code = code + generate_resolver(endpoint)
        code = code + "\n"
        code = code + generate_connectors(endpoint) + "\n"

    return code

f = open("code.py", "w")
f.write(code_generator(endpoints))

#print(code_generator(endpoints))

