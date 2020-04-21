#!/usr/local/bin/python3
#
# updateReport.py
# Xavier Bizoux, GEL
# April 2020
#
# Update a report using information extracted from a source
# environment using getReportContent.py sample code.
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
#### ./createReport.py  -u myAdmin                              ####
####                    -p myAdminPW                            ####
####                    -sn http://myServer.sas.com             ####
####                    -an app                                 ####
####                    -as appsecret                           ####
####                    -i  /tmp/CICD/CarsReport.json           ####
####################################################################

import json
import argparse
from viyaRestPy.Reports import getReport, updateReportContent

# Define arguments for command line execution
parser = argparse.ArgumentParser(
    description="Import report in a target environment")
parser.add_argument("-u",
                    "--user",
                    help="User used for the Viya connection and who will update the preferences.",
                    required=True)
parser.add_argument("-p",
                    "--password",
                    help="Password for the administrative user.",
                    required=True)
parser.add_argument("-sn",
                    "--servername",
                    help="URL of the Viya environment (including protocol and port).",
                    required=True)
parser.add_argument("-an",
                    "--applicationname",
                    help="Name of the application defined based on information on https://developer.sas.com/apis/rest/",
                    required=True)
parser.add_argument("-as",
                    "--applicationsecret",
                    help="Secret for the application based on information on https://developer.sas.com/apis/rest/",
                    required=True)
parser.add_argument("-i",
                    "--input",
                    help="File to collect the report information. For example a GIT repository location",
                    required=True)


# Read the arguments from the command line
args = parser.parse_args()
inFile = args.input

# Collect information needed for authentication
authInfo = {}
if args.user:
    authInfo["user"] = args.user
if args.password:
    authInfo['pw'] = args.password
if args.servername:
    authInfo["serverName"] = args.servername
if args.applicationname:
    authInfo["appName"] = args.applicationname
if args.applicationsecret:
    authInfo["appSecret"] = args.applicationsecret

# Read the input file containing the report information
with open(inFile) as input:
    data = json.load(input)

# Update the report using the information from the source file
updateReportContent(
    data["content"],
    name=data["name"],
    path=data["location"],
    auth=authInfo)

