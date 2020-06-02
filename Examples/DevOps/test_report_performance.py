#!/usr/local/bin/python3
#
# testReportPerformance.py
# Xavier Bizoux, GEL
# April 2020
#
# Test report as part of a CI/CD process
#
# Change History
#
# sbxxab 20APR2020
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
#### ./testReportPerformance.py -u  myAdmin                     ####
####                            -p  myAdminPW                   ####
####                            -sn http://myServer.sas.com:80  ####
####                            -an app                         ####
####                            -as appsecret                   ####
####                            -i  /tmp/CICD/CarsReport.json   ####
####################################################################
# Import modules
import json
import argparse
import os
from viyaRestPy.Reports import get_report_image

# Define arguments for command line execution
parser = argparse.ArgumentParser(
    description="Retrieve an image from the first page of the report as part of CI/CD process")
parser.add_argument("-u",
                    "--user",
                    help="User used for the Viya connection.",
                    required=False)
parser.add_argument("-p",
                    "--password",
                    help="Password for the user.",
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


# Read information from the JSON file
with open(in_file) as input:
    data = json.load(input)

# Generate an image from the first section of the report
report_image = get_report_image(
    name=data["name"],
    path=data["location"],
    auth=auth_info)

# Collect performance data from the image generation
perf_data = {
    "testDate": report_image["json"]["creationTimeStamp"],
    "duration": report_image["json"]["duration"]
}

# Write the performance data to the perf file of the report.
# If the file doesn't exist, it will be created automatically.
out_file = in_file.replace(".json", ".perf")
if os.path.isfile(out_file):
    with open(out_file) as out:
        data = json.load(out)
        data["performance"].append(perf_data)
else:
    data = {"name": data["name"],
            "location": data["location"], "performance": [perf_data]}

with open(out_file, "w") as out:
    json.dump(data, out)
