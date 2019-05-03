import schema2

import graphql



print(type(schema2.schema.get_query_type().fields['users'].resolver))