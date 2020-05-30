import sys
import requests
from .Authentication import generateAuthToken, readAuthToken, readOAuthToken

oauthToken = {}

def callRest(endpoint, method, params={}, headers={"acceptType": "application/json", "contentType": "application/json"}, data={}, auth={}):
    global oauthToken
    # define list of valid methods
    validMethods = ["get", "post", "delete", "put"]
    if oauthToken == {}:
        if bool(auth):
            if len(auth) == 5:
                oauthToken = generateAuthToken(auth)
            elif len(auth) == 1 and bool(auth["serverName"]):
                oauthToken = readOAuthToken(auth["serverName"])
        else:
            oauthToken = readAuthToken()
    # execute requests
    url = oauthToken["baseUrl"] + endpoint
    headers.update({"authorization": 'bearer ' + oauthToken["token"]})
    if method in validMethods:
        response = requests.request(
            method,
            url,
            headers=headers,
            params=params,
            json=data)
        if (400 <= response.status_code <= 599):
            print("ERROR:{0:s}".format(response.text))
            sys.exit()
        else:
            result = {
                'json': {},
                'headers': response.headers
            }
            if method in ["get", "post"]:
                try:
                    result["json"] = response.json()
                except ValueError:
                    print("The request did not return a JSON formatted string")
                    print("The request returned: {0:s}".format(response.text))
                    sys.exit()
            return result
    else:
        print("NOTE: {0:s} method is invalid. Valid methods are: {1:s}.".format(
            method, ', '.join(map(str, validMethods))))