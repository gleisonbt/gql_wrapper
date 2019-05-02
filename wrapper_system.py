import json
from pattern.text.en import singularize

print(singularize('repos'))

#https://api.github.com/users/gleisonbt/repos
with open('repos.json') as json_file:
    data = json.load(json_file)

    if type(data) == list:
        for key in data[0].keys():
            print(key + " - " + str(type(data[0][key])))
            