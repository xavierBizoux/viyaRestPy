import sys
import requests

def generateAuthToken(authInfo):
    global oauthToken
    # Function to authenticate the administrative user and get the authentication token
    url = "{0:s}/SASLogon/oauth/token".format(authInfo["serverName"])
    data = {"grant_type": "password",
            "username": authInfo["user"],
            "password": authInfo["pw"]}
    auth = (authInfo["appName"], authInfo["appSecret"])
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(
        url,
        data=data,
        auth=auth,
        headers=headers)
    if (400 <= response.status_code <= 599):
        print("ERROR:{0:s}".format(response.text))
        sys.exit()
    else:
        oauthToken = {
            "baseUrl": authInfo["serverName"],
            "token": response.json()['access_token']
        }
        return oauthToken
