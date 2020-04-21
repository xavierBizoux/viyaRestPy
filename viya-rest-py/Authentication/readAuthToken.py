import os
import sys
import json
from datetime import datetime
from SASDEVOPSPY.Authentication import getBaseUrl

def readAuthToken():
    global oauthToken
    # get baseUrl
    baseUrl = getBaseUrl()
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

    curProfile = os.environ.get("SAS_CLI_PROFILE", "Default")
    if curProfile in data:
        if datetime.strptime(data[curProfile]["expiry"][:-1], "%Y-%m-%dT%H:%M:%S") > datetime.now():
            oauthToken= {
                "baseUrl": baseUrl,
                "token": data[curProfile]['access-token']
            }
            return oauthToken
        else:
            print(
                "ERROR: cannot connect to {0:s} , your token expired".format(baseUrl))
            print("ERROR: Try refreshing your token with sas-admin auth login")
            sys.exit()
    else:
        print("ERROR: access token for profile '{0:s}' not in file: {1:s}".format(
            curProfile, credential_file))
        print("ERROR: Try refreshing your token with sas-admin auth login")
        sys.exit()