import sys
import requests
from .Authentication import generate_auth_token, read_auth_token, read_oauth_token

oauth_token = {}

def call_rest(endpoint, method, params={}, headers={"acceptType": "application/json", "contentType": "application/json"}, data={}, auth={}):
    global oauth_token
    # define list of valid methods
    valid_methods = ["get", "post", "delete", "put"]
    if oauth_token == {}:
        if bool(auth):
            if len(auth) == 5:
                oauth_token = generate_auth_token(auth)
            elif len(auth) == 1 and bool(auth["server_name"]):
                oauth_token = read_oauth_token(auth["server_name"])
        else:
            oauth_token = read_auth_token()
    # execute requests
    url = oauth_token["base_url"] + endpoint
    headers.update({"authorization": 'bearer ' + oauth_token["token"]})
    if method in valid_methods:
        response = requests.request(
            method,
            url,
            headers=headers,
            params=params,
            json=data,
            verify=False)
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
            method, ', '.join(map(str, valid_methods))))