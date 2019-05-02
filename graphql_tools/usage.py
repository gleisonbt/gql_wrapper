import graphql
import json

from graphql_tools import build_executable_schema

source_schema = """
    schema {
      query: RootQuery
    }
    type RootQuery {
      officers: [Officer]
    }
    
    type Officer {
      title: String
      first: String
      last: String
      uniform: Uniform
    }
    type Uniform {
      pips: Float
    }
"""

resolvers = {
  'RootQuery': {
    # returning direct values, but would normally load fetch db with some info.context
    'officers': lambda value, info, **args: [
        dict(first='william', last='riker'), 
        dict(first='geordi', last='laforge'),
    ]  
  },
  'Officer': {
      # only declaring the field here which is computed
      'title': lambda value, info, **args: 'Officer: %(first)s %(last)s' % value,
      # and the connection
      'uniform': lambda value, info, **args: value['first']=='geordi' and {'i':2.5} or {'i':3},
  },
  'Uniform': {
      'pips': lambda value, info, **args: value['i'],
  }
}


my_schema = build_executable_schema(source_schema, resolvers)

executed = graphql.graphql(my_schema, """
    query Example {
       officers {
         first
         last
         title
         uniform { pips }
       }
    }
""")

print(json.dumps(executed.data, indent=4))