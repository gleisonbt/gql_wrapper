import json


endpoints = []

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


function_list = []

def generate_resolver(endpoint):
    function_name = name_root_node(endpoint)

    function_list.append(function_name)

    if function_list.count(function_name) > 1:
        function_name = function_name + '_' + str(function_list.count(function_name) -1)

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

    if rest[len(rest)-1] == '+':
        rest = rest[0:len(rest)-1]

    resolver_string = resolver_string + " " + function_name + "(self, info, " + params + "):\n"
    resolver_string = resolver_string + "\t" + "entry = restCall(" + rest + ")\n"
    resolver_string = resolver_string + "\t" + "return json2obj(json.dumps(entry))"

    return resolver_string

connector_list = []
def generate_connectors(endpoint):
    connector_name = name_root_node(endpoint)
    connector_list.append(connector_name)
    if connector_list.count(connector_name) > 1:
        connector_name = connector_name + '_' + str(connector_list.count(connector_name) -1)
    return "schema.get_query_type().fields[\'" + connector_name + "\'].resolver = " + connector_name



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

f.close()\n"""

    for endpoint in endpoints:
        code = code + generate_resolver(endpoint)
        code = code + "\n"
        code = code + generate_connectors(endpoint) + "\n"
    
    f = open("wrapper.py", "w")
    f.write(code)

    #return code

def server_gererator():
    server = """
from flask import Flask
from flask_graphql import GraphQLView
import os
import wrapper


view_func = GraphQLView.as_view(
     'graphql', schema=wrapper.schema, graphiql=True)

app = Flask(__name__)
app.add_url_rule('/graphiql', view_func=view_func)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 5000))"""
    f = open("server.py", "w")
    f.write(server)


