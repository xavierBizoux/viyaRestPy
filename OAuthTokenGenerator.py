import requests
import os
import sys
import json
import webbrowser
import platform
from flask import Flask, render_template, request

consulToken = ""
host = ""
appName = ""
appSecret = ""
credentialsFile = ""


def generateIDToken(hostname, consulToken):
    endpoint = "/SASLogon/oauth/clients/consul?callback=false&serviceId=app"
    headers = {"X-Consul-Token": consulToken}
    response = requests.post(hostname+endpoint, headers=headers, verify=False)
    accessToken = response.json()["access_token"]
    return accessToken


def generateApp(hostname, consulToken, clientId, clientSecret):
    global host
    global appName
    global appSecret
    host = hostname
    appName = clientId
    appSecret = clientSecret
    idToken = generateIDToken(hostname, consulToken)
    endpoint = "/SASLogon/oauth/clients"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + idToken
    }
    data = {
        "client_id": clientId,
        "client_secret": clientSecret,
        "scope": ["openid", "*"],
        "authorized_grant_types": ["authorization_code", "refresh_token"],
        "redirect_uri": "http://127.0.0.1:5000/accessToken"
    }
    requests.post(hostname + endpoint, headers=headers, json=data, verify=False)
    url = "{0}/SASLogon/oauth/authorize?client_id={1}&response_type=code".format(
        hostname,
        appName)
    webbrowser.open(url, new=0)


def generateAccessToken(hostname, code, appName, appSecret):
    global credentialsFile
    endpoint = "/SASLogon/oauth/token"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    auth = (appName, appSecret)
    data = {
        "grant_type": "authorization_code",
        "code": code
    }
    response = requests.get(
        hostname + endpoint,
        headers=headers,
        params=data,
        auth=auth, verify=False)
    if platform.system == "Windows":
        credentialsFile = os.path.join(
            os.path.expanduser('~'),
            '_sasauthinfo')
    else:
        credentialsFile = os.path.join(
            os.path.expanduser('~'),
            '.sas',
            '.sasauthinfo')
    try:
        with open(credentialsFile, "r+") as inFile:
            inData = json.loads(inFile.read())
            inData.update({hostname: response.json()})
    except:
        inData = {hostname: response.json()}
    try:
        with open(credentialsFile, "w+") as outFile:
            json.dump(inData, outFile)
    except:
        print("ERROR: Cannot write updated authentication information to: ", credentialsFile)
        sys.exit()
    return(response.json())


app = Flask(__name__)


@app.route("/", methods=['POST', 'GET'])
def displayForm():
    if request.method == 'GET':
        return render_template("OAuthTokenGenerator.html")
    else:
        generateApp(request.form['hostname'],
                    request.form["consulToken"],
                    request.form["client_id"],
                    request.form["client_secret"])
        return 'Processing!'


@app.route("/accessToken")
def displayAuthorizationCode():
    global host
    global appName
    global appSecret
    generateAccessToken(
        host,
        request.args.get('code'),
        appName,
        appSecret)
    return "The token has been generated properly and a copy has been saved under " + credentialsFile + ".\n To apply correct security on that file, please follow the instructions in <a href='https://go.documentation.sas.com/?docsetId=authinfo&docsetTarget=n0xo6z7e98y63dn1fj0g9l2j7oyq.htm&docsetVersion=9.4&locale=en#n1stv9zynsyf6rn1wbr3ejga6ozf' target='_blank' rel='noopener noreferrer'>this link</a>"
