import os
import sys
import json
from datetime import datetime
from .get_base_url import get_base_url


def read_auth_token():
    global oauth_token
    base_url = get_base_url()
    # get authentication information for the header
    credential_file = os.path.join(
        os.path.expanduser('~'), '.sas', 'credentials.json')
    try:
        with open(credential_file) as json_file:
            data = json.load(json_file)
    except:
        print("ERROR: Cannot read authentication credentials at: ", credential_file)
        print("ERROR: Try refreshing your token with sas-admin auth login")
        sys.exit()

    current_profile = os.environ.get("SAS_CLI_PROFILE", "Default")
    if current_profile in data:
        if datetime.strptime(data[current_profile]["expiry"][:-1], "%Y-%m-%dT%H:%M:%S") > datetime.now():
            oauth_token = {
                "baseUrl": base_url,
                "token": data[current_profile]['access-token']
            }
            return oauth_token
        else:
            print(
                "ERROR: cannot connect to {0:s} , your token expired".format(base_url))
            print("ERROR: Try refreshing your token with sas-admin auth login")
            sys.exit()
    else:
        print("ERROR: access token for profile '{0:s}' not in file: {1:s}".format(
            current_profile, credential_file))
        print("ERROR: Try refreshing your token with sas-admin auth login")
        sys.exit()
