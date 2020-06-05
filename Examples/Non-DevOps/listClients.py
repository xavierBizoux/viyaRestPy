import requests
from viyaRestPy import call_rest

server_name = "http://rext03-0109.race.sas.com"
endpoint = "/SASLogon/oauth/clients"

auth_info = {}
auth_info["server_name"] = server_name
params = {}

clients = call_rest(endpoint, "get", params=params, auth=auth_info)

print(clients)