from graphene import ObjectType, String, Boolean, ID, List, Field, Int, List, DateTime, Schema
import json
import os
from collections import namedtuple
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

class Users(ObjectType):
    login = String()
    id = ID()
    node_id = String()
    avatar_url = String()
    gravatar_id = String()
    html_url = String()
    type = String()
    site_admin = Boolean()

class User(ObjectType):
    login = String()
    id = ID()
    node_id = String()
    avatar_url = String()
    gravatar_id = String()
    html_url = String()
    type = String()
    site_admin = Boolean()
    name = String()
    company = String()
    blog = String()
    location = String()
    email = String()
    hireable = Boolean()
    bio = String()
    public_repos = Int()
    public_gists = Int()
    followers = Int()
    following = Int()
    created_at = String()
    updated_at = String()



class Query(ObjectType):
    users = List(Users, since=Int(required=True), per_page=Int(required=True), page=Int(required=True))

    def resolve_users(self, info, since, per_page, page):
        entries = restCall('https://api.github.com/users?since=' + str(since) + "&per_page=" + str(per_page) + "&page=" + str(page))
        return json2obj(json.dumps(entries))

    user = Field(User, username=String(required=True))

    def resolve_user(self, info, username):
        entry = restCall('https://api.github.com/users/' + str(username))
        return json2obj(json.dumps(entry))

    # getListOfPapers = List(Paper, search_query=String(required=True), max_results=Int(required=True), start=Int(required=True),
    #             sort_by=String(required=False), sort_order=String(required=False))
    
    # def resolve_getListOfPapers(self, info, search_query, max_results, start, sort_by, sort_order):
    #     entries = arxiv.query(search_query=search_query,id_list=[],max_results=max_results, start=start, sort_by=sort_by, sort_order=sort_order)
    #     return json2obj(json.dumps(entries))
    
    # getPaper = Field(Paper, id=ID(required=True))

    # def resolve_getPaper(self, info, id):
    #     entry = arxiv.query(id_list=[id])
    #     return json2obj(json.dumps(entry))[0]

my_schema = Schema(
    query=Query, types=[Users, User]
)




















