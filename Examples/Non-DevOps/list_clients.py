import requests


deletion = False
hostname = "http://intviya01.race.sas.com"
endpoint = "/SASLogon/oauth/clients/consul?callback=false&serviceId=app"
consul_token = "6fd548ac-d899-4be5-9fd6-62111f1ab7b5"
url = hostname + endpoint
headers = {"X-Consul-Token": consul_token}
response = requests.post(url, headers=headers, verify=False)
clients_endpoint = "/SASLogon/oauth/clients"
clients_url = hostname + clients_endpoint
clients_headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + response.json()["access_token"]
    }
list_clients = requests.get(clients_url, headers=clients_headers)


for client in list_clients.json()["resources"]:
        #if client["client_id"] == "app":
        print(client["client_id"])
        if deletion == True:
            if "redirect_uri" in client and client["redirect_uri"] == ['http://127.0.0.1:5000/accessToken']:
                delete_url = "{0}{1}/{2}".format(hostname, clients_endpoint, client["client_id"])
                delete_response = requests.delete(delete_url, headers=clients_headers, verify=False)
                print(delete_response)