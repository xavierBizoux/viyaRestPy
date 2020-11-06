import sys
import os
import json
import requests


def refresh_token(hostname, current_info, credentials_file):
    global oauth_token
    url = "{0}/SASLogon/oauth/token".format(hostname)
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    }
    data = {
        "grant_type": "refresh_token",
        "refresh_token": current_info["refresh_token"]
    }
    auth = (current_info["client_id"], current_info["client_secret"])
    response = requests.post(url, headers=headers, data=data, auth=auth, verify=False)
    oauth_token.update({"token": response.json()["access_token"]})
    try:
        with open(credentials_file, "r") as in_file:
            in_data = json.loads(in_file.read())
    except:
        print("ERROR: Cannot open authentication credentials at: ", credentials_file)
        sys.exit()
    in_data.update({hostname: response.json()})
    try:
        with open(credentials_file, "w") as out_file:
            json.dump(in_data, out_file)
            print("updated")
    except:
        print("ERROR: Cannot write updated authentication information to: ",
              credentials_file)
        sys.exit()


def read_oauth_token(hostname):
    global oauth_token
    credentials_file = os.path.join(
        os.path.expanduser('~'), '.sas', '.sasauthinfo')
    try:
        with open(credentials_file, 'r') as in_file:
            data = json.loads(in_file.read())
    except:
        print("ERROR: Cannot read authentication credentials at: ", credentials_file)
        sys.exit()
    if bool(data[hostname]):
        oauth_token = {
            "base_url": hostname,
            "token": data[hostname]["access_token"]
        }
        headers = {"authorization": 'bearer ' +
                   oauth_token["token"], "Accept": "application/json"}
        test = requests.get(
            oauth_token["base_url"] + "/folders/folders/@myFolder", headers=headers, verify=False)
        if test.status_code == 401:
            print("NOTE: Refreshing token")
            refresh_token(hostname, data[hostname], credentials_file)
        return oauth_token
    if oauth_token == {}:
        print("There is no information for {0} in {1}.".format(
            hostname, credentials_file))
