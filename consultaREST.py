import requests

URL = 'https://api.github.com/'
token = '773e67ef75e7274d5eef5722b1e714cc6c6770cc' #gleison


def restCall(query, token=token):
    r = requests.get(URL + query, headers={'Authorization': 'Bearer '+ token})
    print(r.status_code)
    return r



r = restCall('search/repositories?q=stars:0..*+language:c&sort=stars&order=desc&page=1&per_page=100')

print(r.json())