import json
import requests

token = '773e67ef75e7274d5eef5722b1e714cc6c6770cc' #gleison

URL = 'https://api.github.com' 

def restCall(query, token=token):
    r = requests.get(query, headers={'Authorization': 'Bearer '+ token})
    return r.json()

endpoints = [
    {
        'path':'/users/{username}/repos',
        'parameters':[{'type':'string'},{'sort':'string'},{'direction':'string'}],
        'example':'https://api.github.com/users/gleisonbt/repos'
    },
    {
        'path':'/users/{username}/starred',
        'parameters':[{'type':'string'},{'sort':'string'},{'direction':'string'}],
        'example':'https://api.github.com/users/gleisonbt/starred'
    }
]

# [
#     'https://api.github.com/users/facebook/repos',
#     'https://api.github.com/users/gleisonbt/starred'
# ]

def name_root_node(endpoints):
    


def generate_schema(endpoints):
    for endpoint in endpoints:
        data = restCall(endpoint['example'])

        json2graphql(data, "")

#data = restCall('https://api.github.com/users/facebook/repos?type=all&page=1&per_page=10&order=desc&sort=created_at')


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
    elif type_class == dict:
        return key[0].upper() + key[1:len(key)]
    elif type_class == list:
        return '[' + parseTypes(key, value[0]) + ']'
    
    

def json2graphql(json, rootType):
    schema = ""
    if type(json) == list:
        data = json[0]
    else:
        data = json
     
    schema = schema + "type " + rootType + " {" + "\n"
    
    for key in data.keys():
        schema = schema + '\t' + key + ": " + parseTypes(key, data[key]) + '\n'
        if type(data[key]) == dict:
            schema = json2graphql(data[key], parseTypes(key, data[key])) + schema

    schema = schema + '}' + '\n'
    return schema
    


print(schema)

