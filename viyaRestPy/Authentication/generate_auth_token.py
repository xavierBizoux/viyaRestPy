import sys
import requests


def generate_auth_token(auth_info):
    global oauth_token
    # Function to authenticate the administrative user and get the authentication token
    url = "{0:s}/SASLogon/oauth/token".format(auth_info["server_name"])
    data = {"grant_type": "password",
            "username": auth_info["user"],
            "password": auth_info["pw"]}
    auth = (auth_info["app_name"], auth_info["app_secret"])
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(
        url,
        data=data,
        auth=auth,
        headers=headers,
        verify=False)
    if (400 <= response.status_code <= 599):
        print("ERROR:{0:s}".format(response.text))
        sys.exit()
    else:
        oauth_token = {
            "base_url": auth_info["server_name"],
            "token": response.json()['access_token']
        }
        return oauth_token
