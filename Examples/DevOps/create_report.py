#!/usr/local/bin/python3
#
# create_report.py
# Xavier Bizoux, GEL
# March 2020
#
# Create a report using report data extracted from a source
# environment using get_reportContent.py sample code.
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
#### ./create_report.py -u myAdmin                              ####
####                    -p myAdminPW                            ####
####                    -sn http://myServer.sas.com             ####
####                    -an app                                 ####
####                    -as appsecret                           ####
####                    -i  /tmp/CICD/CarsReport.json           ####
####################################################################

import json
import argparse
from viyaRestPy.Reports import create_report

# Define arguments for command line execution
parser = argparse.ArgumentParser(
    description="Import report in a target environment")
parser.add_argument("-u",
                    "--user",
                    help="User used for the Viya connection and who will update the preferences.",
                    required=False)
parser.add_argument("-p",
                    "--password",
                    help="Password for the administrative user.",
                    required=False)
parser.add_argument("-sn",
                    "--servername",
                    help="URL of the Viya environment (including protocol and port).",
                    required=True)
parser.add_argument("-an",
                    "--applicationname",
                    help="Name of the application defined based on information on https://developer.sas.com/apis/rest/",
                    required=False)
parser.add_argument("-as",
                    "--applicationsecret",
                    help="Secret for the application based on information on https://developer.sas.com/apis/rest/",
                    required=False)
parser.add_argument("-i",
                    "--input",
                    help="File to collect the report information. For example a GIT repository location",
                    required=True)


# Read the arguments from the command line
args = parser.parse_args()
in_file = args.input

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

# Read the input file containing the report information
with open(in_file) as input:
    data = json.load(input)

# Create the report based on the input file data
report = create_report(
    name=data["name"],
    path=data["location"],
    content=data["content"],
    auth=auth_info)
