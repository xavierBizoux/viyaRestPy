#!/usr/local/bin/python3
#
# get_report.py
# Xavier Bizoux, GEL
# April 2020
#
# Extract report information to be used in a CI/CD process
#
# Change History
#
# sbxxab 17APR2020
#
####################################################################
#### DISCLAIMER                                                 ####
####################################################################
#### This program  provided as-is, without warranty             ####
#### of any kind, either express or implied, including, but not ####
#### limited to, the implied warranties of merchantability,     ####
#### fitness for a particular purpose, or non-infringement.     ####
#### SAS Institute shall not be liable whatsoever for any       ####
#### damages arising out of the use of this documentation and   ####
#### code, including any direct, indirect, or consequential     ####
#### damages. SAS Institute reserves the right to alter or      ####
#### abandon use of this documentation and code at any time.    ####
#### In addition, SAS Institute will provide no support for the ####
#### materials contained herein.                                ####
####################################################################

####################################################################
#### COMMAND LINE EXAMPLE                                       ####
####################################################################
#### ./get_report.py        -u  myUser                          ####
####                        -p  myPW                            ####
####                        -sn http://myServer.sas.com:80      ####
####                        -an app                             ####
####                        -as appsecret                       ####
####                        -rl "/Users/sbxxab/My Folder"       ####
####                        -rn CarsReport                      ####
####                        -o  /tmp/CICD/                      ####
####################################################################
# Import modules
import json
import argparse
import sys
from viyaRestPy.Reports import get_report_content

# Define arguments for command line execution
parser = argparse.ArgumentParser(
    description="Extract report information to be used in a CI/CD process")
parser.add_argument("-rl",
                    "--reportlocation",
                    help="Location of the report within SAS Viya",
                    required=True)
parser.add_argument("-rn",
                    "--reportname",
                    help="Name of the report within SAS Viya",
                    required=True)
parser.add_argument("-o",
                    "--output",
                    help="Path to save the report information. For example a GIT repository location",
                    required=True)
parser.add_argument("-u",
                    "--user",
                    help="Authentication: User used for the Viya connection.",
                    required=False)
parser.add_argument("-p",
                    "--password",
                    help="Authentication: Password for the user.",
                    required=False)
parser.add_argument("-sn",
                    "--servername",
                    help="Authentication: URL of the Viya environment (including protocol and port).",
                    required=False)
parser.add_argument("-an",
                    "--applicationname",
                    help="Authentication: Name of the application defined based on information on https://developer.sas.com/apis/rest/",
                    required=False)
parser.add_argument("-as",
                    "--applicationsecret",
                    help="Authentication: Secret for the application based on information on https://developer.sas.com/apis/rest/",
                    required=False)

# Read the arguments from the command line
args = parser.parse_args()
report_location = args.reportlocation
report_name = args.reportname
out_folder = args.output

# Collect information needed for authentication
auth_info = {}
if args.user:
    auth_info["user"] = args.user
if args.password:
    auth_info['pw'] = args.password
if args.servername:
    auth_info["server_name"] = args.servername
if args.applicationname:
    auth_info["app_name"] = args.applicationname
if args.applicationsecret:
    auth_info["app_secret"] = args.applicationsecret

report_content = get_report_content(
    report_name,
    path=report_location,
    auth=auth_info)

# Create a JSON representation of the report
data = {"name": report_name,
        "location": report_location,
        "content": report_content["json"]}

# Generate output file
out_file = out_folder + report_name + ".json"
with open(out_file, "w") as out:
    json.dump(data, out)
