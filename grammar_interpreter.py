from textx import metamodel_from_str, get_children_of_type

grammar = """
Program:
    URL
    Token
    paths*=Path
;

URL:
    'URL: ' url = /[a-zA-Z0-9_$\/\\\%\&\*\.\!\:]+/
;

Token:
    'Token: ' token = /^|[a-zA-Z0-9_$]+/ 
;

Path:
    'Path 'name=/[a-zA-Z0-9_]+/':'
        'rout: ' rout=/(\/([[A-Za-z0-9_]+\:(string|int))|\/[A-Za-z0-9_]+)+/
        'params: ' params*=/None|([a-zA-Z0-9_]+\:(string|int))/[',']
        'example: ' example=/(\/[A-Za-z0-9_]+)+/
        paths*=Path
    'end'
;
"""

class Endpoint(object):
    def __init__(self, name, rout, params, example):
        self.name = name
        self.rout = rout
        self.params = params
        self.example = example
    


mm = metamodel_from_str(grammar, classes=[Endpoint])

model_str = """
URL: https://api.github.com
Token: dsfsdfs
Path Users:
    rout: /users
    params: since:int
    example: /users
    Path xxx:
        rout: /username:string
        params: dfsf:int
        example: /bla
        Path yyy:
            rout: /lalala
            params: uuuu:string, rerer:int
            example: /ble    
        end
    end
end
Path Repos:
    rout: /repos
    params: owner:string, repo:string
    example: /bla
end
"""

model = mm.model_from_str(model_str)

def cname(o):
    return o.__class__.__name__


endpoints = []


def endpoint_object_creation(path, previous_rout):
    rout = previous_rout + path.rout 
    endpoint = Endpoint(path.name, rout, path.params, path.example)

    endpoints.append(endpoint)

    for path in path.paths:
        endpoint_object_creation(path, rout)
     

for path in model.paths:
    endpoint_object_creation(path, "")



# json = "["

# for endpoint in endpoints:
#     json = json + """
#     {
#     """
#     json = json + "\t\"rout\":" + "\"" + endpoint.rout + "\""
#     json = json + """
#     }"""

# json = json + "\n]"

# print(json)

# f = open("endpoints.txt", "w")
# f.write(json)