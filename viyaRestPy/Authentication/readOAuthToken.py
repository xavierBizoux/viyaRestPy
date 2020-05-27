import sys
import os
import json
import requests


def refreshToken(hostname, currentInfo, credentialsFile):
    global oauthToken
    url = "{0}/SASLogon/oauth/token".format(hostname)
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    }
    data = {
        "grant_type": "refresh_token",
        "refresh_token": currentInfo["refresh_token"]
    }
    auth = ("gelApp", "lnxsas")
    response = requests.post(url, headers=headers, data=data, auth=auth)
    oauthToken.update({"token": response.json()["access_token"]})
    try:
        with open(credentialsFile, "r") as inFile:
            inData = json.loads(inFile.read())
    except:
        print("ERROR: Cannot open authentication credentials at: ", credentialsFile)
        sys.exit()
    inData.update({hostname: response.json()})
    try:
        with open(credentialsFile, "w") as outFile:
            json.dump(inData, outFile)
    except:
        print("ERROR: Cannot write updated authentication information to: ", credentialsFile)
        sys.exit()


def readOAuthToken(hostname):
    global oauthToken
    credentialsFile = os.path.join(
        os.path.expanduser('~'), '.sas', '.sasauthinfo')
    try:
        with open(credentialsFile, 'r') as inFile:
            data = json.loads(inFile.read())
    except:
        print("ERROR: Cannot read authentication credentials at: ", credentialsFile)
        sys.exit()
    if bool(data[hostname]):
        oauthToken = {
            "baseUrl": hostname,
            "token": data[hostname]["access_token"]
        }
        headers = {"authorization": 'bearer ' +
                   oauthToken["token"], "Accept": "application/json"}
        test = requests.get(
            oauthToken["baseUrl"] + "/folders/folders/@myFolder", headers=headers)
        if test.status_code == 401:
            print("NOTE: Refreshing token")
            refreshToken(hostname, data[hostname], credentialsFile)
        return oauthToken
    if oauthToken == {}:
        print("There is no information for {0} in {1}.".format(
            hostname, credentialsFile))