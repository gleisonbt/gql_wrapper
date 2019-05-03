

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

schema = parse_schema(
"""
schema {
  query: Query
}

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


def get_users(self, info, since, perPage, page):
  entries = restCall('https://api.github.com/users?since=' + str(since) + "&per_page=" + str(perPage) + "&page=" + str(page))
  return json2obj(json.dumps(entries))

def get_user(self, info, username):
  entry = restCall('https://api.github.com/users/' + str(username))
  return json2obj(json.dumps(entry))


schema.get_query_type().fields['users'].resolver = get_users
schema.get_query_type().fields['user'].resolver = get_user




# my_schema = Schema(
#     # query=Query, types=[Paper, TitleDetail, ArxivPrimaryCategory, Tag, AuthorDetail]
# )




















