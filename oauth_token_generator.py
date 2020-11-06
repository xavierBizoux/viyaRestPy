import requests
import os
import sys
import json
import webbrowser
import platform
import urllib.parse
from flask import Flask, render_template, request

consul_token = ""
host = ""
app_name = ""
app_secret = ""
credentials_file = ""


def generate_id_token(hostname, consul_token, app_name):
    endpoint = "/SASLogon/oauth/clients/consul?callback=false&serviceId={0}".format(
        app_name)
    url = hostname + endpoint
    headers = {"X-Consul-Token": consul_token}
    response = requests.post(url, headers=headers, verify=False)
    access_token = response.json()["access_token"]
    return access_token


def generate_app(hostname, consul_token, client_id, client_secret):
    global host
    global app_name
    global app_secret
    host = hostname
    app_name = client_id
    app_secret = client_secret
    id_token = generate_id_token(hostname, consul_token, app_name)
    endpoint = "/SASLogon/oauth/clients"
    url = hostname + endpoint
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
    client_url = "{0}{1}/{2}".format(host, endpoint, app_name)
    check_client = requests.head(client_url, headers=headers, verify=False)
    if check_client.status_code == 200:
        client = requests.get(client_url, headers=headers, verify=False).json()
        if "authorization_code" in client["authorized_grant_types"] and "redirect_uri" in client and client["redirect_uri"] == ['http://127.0.0.1:5000/accessToken']:
            browser_url = "{0}/SASLogon/oauth/authorize?response_type=code&client_id={1}".format(
                hostname,
                app_name)
            webbrowser.open(browser_url, new=0)
            return "generate"
        else:
            return "exist"
    else:
        requests.post(url, headers=headers, json=data, verify=False)
        browser_url = "{0}/SASLogon/oauth/authorize?response_type=code&client_id={1}".format(
            hostname,
            app_name)
        webbrowser.open(browser_url, new=0)
        return "create"


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
        auth=auth,
        verify=False)
    auth_data = response.json()
    auth_data.update({"client_id": app_name})
    auth_data.update({"client_secret": app_secret})
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
            in_data.update({hostname: auth_data})
    except:
        in_data = {hostname: auth_data}
    try:
        with open(credentials_file, "w+") as out_file:
            json.dump(in_data, out_file)
    except:
        print("ERROR: Cannot write updated authentication information to: ",
              credentials_file)
        sys.exit()
    return(response.json())


app = Flask(__name__)


@app.route("/", methods=['POST', 'GET'])
def displayForm():
    message = {}
    if request.method == 'GET':
        message["hostname"] = ""
        message["consul_token"] = ""
        message["client_id"] = ""
        message["client_secret"] = ""
        message["text"] = ""
        return render_template("OAuthTokenGenerator.html", message=message)
    else:
        status = generate_app(request.form['hostname'],
                              request.form["consul_token"],
                              request.form["client_id"],
                              request.form["client_secret"])
        message["hostname"] = request.form['hostname']
        message["consul_token"] = request.form['consul_token']
        message["client_secret"] = request.form['client_secret']
        if status == "exist":
            message["text"] = "The Client Application Name already exists. Please choose another one."
        elif status == "generate":
            message["text"] = "The Client Application Name already exists. Updating the sasauthinfo file."
        else:
            message["client_id"] = request.form['client_id']
            message["text"] = "Creating a new client application with name: {0}".format(
                request.form['client_id'])
        return render_template("OAuthTokenGenerator.html", message=message)


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
