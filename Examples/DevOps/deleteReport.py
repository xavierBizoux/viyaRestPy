#!/usr/local/bin/python3
#
# getReportContent.py
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
#### ./getReportContent.py  -u myAdmin                          ####
####                        -p myAdminPW                        ####
####                        -sn http://myServer.sas.com:80      ####
####                        -an app                             ####
####                        -as appsecret                       ####
####                        -rl "/Users/sbxxab/My Folder"       ####
####                        -rn CarsReport                      ####
####################################################################
# Import modules
import json
import argparse
import sys
from SASDEVOPSPY.Reports import deleteReport

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
parser.add_argument("-u",
                    "--user",
                    help="Authentication: User used for the Viya connection.",
                    required=False)
parser.add_argument("-p",
                    "--password",
                    help="Authentication: Password for the administrater user.",
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
reportLocation = args.reportlocation
reportName = args.reportname

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

deleteReport(
    name=reportName,
    path=reportLocation,
    auth=authInfo)