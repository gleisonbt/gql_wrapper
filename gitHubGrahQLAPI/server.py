from flask import Flask
from flask_graphql import GraphQLView
import os
import schema2


view_func = GraphQLView.as_view(
     'graphql', schema=schema2.schema, graphiql=False)

app = Flask(__name__)
app.add_url_rule('/graphiql', view_func=view_func)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 5000))