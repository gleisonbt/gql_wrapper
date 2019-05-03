import json
import requests
from genson import SchemaBuilder

token = '773e67ef75e7274d5eef5722b1e714cc6c6770cc' #gleison


def restCall(query, token=token):
    r = requests.get(query, headers={'Authorization': 'Bearer '+ token})
    return r.json()

data = restCall('https://api.github.com/users/facebook/repos?type=all&page=1&per_page=10&order=desc&sort=created_at')


def parseTypes(key, type):
    if type == str:
        return 'String'
    elif type == int:
        return 'Int'
    elif str(type.__name__) == 'NoneType':
        return 'String'
    elif type == bool:
        return 'Boolean'
    elif type == dict:
        return key[0].upper() + key[1:len(key)]
    else:
        return str(type)
    

def json2graphql(json, rootType):
    schema = """
    """
    if type(json) == list:
        data = json[0]
    else:
        data = json
    
    print("######### " + rootType + " #############")
    for key in data.keys():
        print(key + ": " + parseTypes(key, type(data[key])))
        schema + key + ": " + parseTypes(key, type(data[key])) + '\n'
        if type(data[key]) == dict:
            json2graphql(data[key], parseTypes(key, type(data[key])))
    
    print("########################################")
    return schema
    

#print("type " + rootType + " {")
#print("}")

schema = json2graphql(data, "userRepos")


