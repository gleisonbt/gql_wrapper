
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
def  reposTrafficClones(self, info, owner, repo):
	entry = restCall('https://api.github.com/repos/'+ str(owner) +'/'+ str(repo) +'/traffic/clones')
	return json2obj(json.dumps(entry))
schema.get_query_type().fields['reposTrafficClones'].resolver = reposTrafficClones
def  reposTrafficViews(self, info, owner, repo):
	entry = restCall('https://api.github.com/repos/'+ str(owner) +'/'+ str(repo) +'/traffic/views')
	return json2obj(json.dumps(entry))
schema.get_query_type().fields['reposTrafficViews'].resolver = reposTrafficViews
def  usersRepos(self, info, username, type, sort, direction):
	entry = restCall('https://api.github.com/users/'+ str(username) +'/repos?type= '+ str(type) +' &sort= '+ str(sort) +' &direction= '+ str(direction))
	return json2obj(json.dumps(entry))
schema.get_query_type().fields['usersRepos'].resolver = usersRepos
def  usersStarred(self, info, username, type, sort, direction):
	entry = restCall('https://api.github.com/users/'+ str(username) +'/starred?type= '+ str(type) +' &sort= '+ str(sort) +' &direction= '+ str(direction))
	return json2obj(json.dumps(entry))
schema.get_query_type().fields['usersStarred'].resolver = usersStarred
def  users(self, info, since, per_page, page):
	entry = restCall('https://api.github.com/users?since= '+ str(since) +' &per_page= '+ str(per_page) +' &page= '+ str(page))
	return json2obj(json.dumps(entry))
schema.get_query_type().fields['users'].resolver = users
def  users_1(self, info, username):
	entry = restCall('https://api.github.com/users/'+ str(username) +'')
	return json2obj(json.dumps(entry))
schema.get_query_type().fields['users_1'].resolver = users_1
