import json
import requests
import random

token = '773e67ef75e7274d5eef5722b1e714cc6c6770cc' #gleison

spotify_token = 'BQDMR8VAgSJj81cvXSdeiKHIHaLqo7KSbdR7OyRkh-Oj6ebUPk5AII2-f3rqm5MYHlsY95wV0GobHQME1Nkm1An5UeLy_H_9AmAJ3AMrE_an-bcimcWLKk8UyMWidw9iP_3yWN99yXp01ghgvIIjGWRN9dc3PcIJgfQ0gtLx0xjah8bLOUT2ke9rWndou892FE3LT9gCTS9v5bQ-vvwwf_qr7TdsMP6IEili58r5kgGAWcAZpN3EDetnieOODbYVFd6pVu23XbJ_O3yT'

URL = 'https://api.github.com' 

def restCall(query, token=token):
    r = requests.get(query, headers={'Authorization': 'Bearer '+ token})
    return r.json()


#print(restCall('https://api.github.com/repos/gleisonbt/DeprecatedFinding/traffic/clones'))

print(restCall('https://api.spotify.com/v1/albums/4aawyAB9vmqN3uQ7FjRGTy?market=ES'))