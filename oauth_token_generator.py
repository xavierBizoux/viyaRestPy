import requests
import os
import sys
import json
import webbrowser
import platform
from flask import Flask, render_template, request

consul_token = ""
host = ""
app_name = ""
app_secret = ""
credentials_file = ""


def generate_id_token(hostname, consul_token):
    endpoint = "/SASLogon/oauth/clients/consul?callback=false&serviceId=app"
    headers = {"X-Consul-Token": consul_token}
    response = requests.post(hostname+endpoint, headers=headers, verify=False)
    access_token = response.json()["access_token"]
    return access_token


def generate_app(hostname, consul_token, client_id, client_secret):
    global host
    global app_name
    global app_secret
    host = hostname
    app_name = client_id
    app_secret = client_secret
    id_token = generate_id_token(hostname, consul_token)
    endpoint = "/SASLogon/oauth/clients"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + id_token
    }
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": ["openid", "*"],
        "authorized_grant_types": ["authorization_code", "refresh_token"],
        "redirect_uri": "http://127.0.0.1:5000/accessToken"
    }
    requests.post(hostname + endpoint, headers=headers, json=data, verify=False)
    url = "{0}/SASLogon/oauth/authorize?client_id={1}&response_type=code".format(
        hostname,
        app_name)
    webbrowser.open(url, new=0)


def generate_access_token(hostname, code, app_name, app_secret):
    global credentials_file
    endpoint = "/SASLogon/oauth/token"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    auth = (app_name, app_secret)
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
        credentials_file = os.path.join(
            os.path.expanduser('~'),
            '_sasauthinfo')
    else:
        credentials_file = os.path.join(
            os.path.expanduser('~'),
            '.sas',
            '.sasauthinfo')
    try:
        with open(credentials_file, "r+") as in_file:
            in_data = json.loads(in_file.read())
            in_data.update({hostname: response.json()})
    except:
        in_data = {hostname: response.json()}
    try:
        with open(credentials_file, "w+") as out_file:
            json.dump(in_data, out_file)
    except:
        print("ERROR: Cannot write updated authentication information to: ", credentials_file)
        sys.exit()
    return(response.json())


app = Flask(__name__)


@app.route("/", methods=['POST', 'GET'])
def displayForm():
    if request.method == 'GET':
        return render_template("OAuthTokenGenerator.html")
    else:
        generate_app(request.form['hostname'],
                    request.form["consul_token"],
                    request.form["client_id"],
                    request.form["client_secret"])
        return 'Processing!'


@app.route("/accessToken")
def displayAuthorizationCode():
    global host
    global app_name
    global app_secret
    generate_access_token(
        host,
        request.args.get('code'),
        app_name,
        app_secret)
    return "The token has been generated properly and a copy has been saved under " + credentials_file + ".\n To apply correct security on that file, please follow the instructions in <a href='https://go.documentation.sas.com/?docsetId=authinfo&docsetTarget=n0xo6z7e98y63dn1fj0g9l2j7oyq.htm&docsetVersion=9.4&locale=en#n1stv9zynsyf6rn1wbr3ejga6ozf' target='_blank' rel='noopener noreferrer'>this link</a>"
