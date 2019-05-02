

import json
import os
from collections import namedtuple

from graphql import build_schema

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

schema = build_schema(
    """
    type Query {
  users(since: Int!, perPage: Int!, page: Int!): [Users]
  user(username: String!): User
}

type User {
  login: String
  id: ID
  nodeId: String
  avatarUrl: String
  gravatarId: String
  htmlUrl: String
  type: String
  siteAdmin: Boolean
  name: String
  company: String
  blog: String
  location: String
  email: String
  hireable: Boolean
  bio: String
  publicRepos: Int
  publicGists: Int
  followers: Int
  following: Int
  createdAt: String
  updatedAt: String
}

type Users {
  login: String
  id: ID
  nodeId: String
  avatarUrl: String
  gravatarId: String
  htmlUrl: String
  type: String
  siteAdmin: Boolean
}
    """
)


def get_users(root, info, since, per_page, page):
    entries = restCall('https://api.github.com/users?since=' + str(since) + "&per_page=" + str(per_page) + "&page=" + str(page))
    return json2obj(json.dumps(entries))

# def get_character_type(character, info):
#         return 'Droid' if character['id'] in droid_data else 'Human'

# def get_Users_type():
#   pass

# def resolve_user(self, info, username):
#     entry = restCall('https://api.github.com/users/' + str(username))
#     return json2obj(json.dumps(entry))


schema.query_type.fields['users'].resolve = get_users
#schema.query_type['Users'].resolve = 




# class Query(ObjectType):
#     users = List(Users, since=Int(required=True), per_page=Int(required=True), page=Int(required=True))

#     def resolve_users(self, info, since, per_page, page):
#         entries = restCall('https://api.github.com/users?since=' + str(since) + "&per_page=" + str(per_page) + "&page=" + str(page))
#         return json2obj(json.dumps(entries))

#     user = Field(User, username=String(required=True))

#     def resolve_user(self, info, username):
#         entry = restCall('https://api.github.com/users/' + str(username))
#         return json2obj(json.dumps(entry))

    # getListOfPapers = List(Paper, search_query=String(required=True), max_results=Int(required=True), start=Int(required=True),
    #             sort_by=String(required=False), sort_order=String(required=False))
    
    # def resolve_getListOfPapers(self, info, search_query, max_results, start, sort_by, sort_order):
    #     entries = arxiv.query(search_query=search_query,id_list=[],max_results=max_results, start=start, sort_by=sort_by, sort_order=sort_order)
    #     return json2obj(json.dumps(entries))
    
    # getPaper = Field(Paper, id=ID(required=True))

    # def resolve_getPaper(self, info, id):
    #     entry = arxiv.query(id_list=[id])
    #     return json2obj(json.dumps(entry))[0]

# my_schema = Schema(
#     # query=Query, types=[Paper, TitleDetail, ArxivPrimaryCategory, Tag, AuthorDetail]
# )




















