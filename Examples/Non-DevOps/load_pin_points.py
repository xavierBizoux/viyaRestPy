#!/usr/local/bin/python3
#
# load_pin_points.py
# Xavier Bizoux, GEL
# April 2020
#
# Load pin points from a source file (csv) to a geo map
#
# Change History
#
# sbxxab 06APR2020
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
#### ./load_pin_points.py   -u myAdmin                          ####
####                        -p myAdminPW                        ####
####                        -sn http://myServer.sas.com:80      ####
####                        -an app                             ####
####                        -as appsecret                       ####
####                        -rl "/Users/sbxxab/My Folder"       ####
####                        -rn CarsReport                      ####
####                        -b  /tmp/CICD/                      ####
####                        -i  /tmp/sasOffices.csv             ####
####################################################################
# Import modules
import json
import argparse
import sys
import csv
from viyaRestPy.Reports import get_report_content, get_report, update_report_content

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
parser.add_argument("-i",
                    "--inputFile",
                    help="File containing the pinpoints information",
                    required=True)
parser.add_argument("-b",
                    "--backupFolder",
                    help="Folder to store a backup of the report",
                    required=True)
parser.add_argument("-u",
                    "--user",
                    help="Authentication: User used for the Viya connection.",
                    required=False)
parser.add_argument("-p",
                    "--password",
                    help="Authentication: Password for the administrative user.",
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
backup_folder = args.backupFolder
in_file = args.inputFile

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

# Extract the content of the existing report
report_content = get_report_content(
    name=report_name,
    path=report_location,
    auth=auth_info)

# Create a backup file of the report
# Create a JSON representation of the report
data = {"name": report_name, "location": report_location,
        "content": report_content["json"]}

# Generate output file
out_file = backup_folder + report_name + ".json"
with open(out_file, "w") as out:
    json.dump(data, out)

# Read pin point information
with open(in_file, newline='') as input_file:
    reader = csv.reader(input_file)
    pin_data = list(reader)
    pin_data.remove(pin_data[0])

# Transform the pin points data to VA report usable information
pin_props = []
for pin_key, pin_point in enumerate(pin_data):
    pin_value = 'Name="{0:s}" Address="{1:s}, {2:s}, {3:s}" LatLon={4:s},{5:s} Type=CUSTOM OriginType=CUSTOM VisualState=DISPLAYED Color=2919126 SelectionMode=NONE IsSelected=true'.format(
        pin_point[0], pin_point[5], pin_point[4], pin_point[3], pin_point[2], pin_point[1])
    pin_prop = {
        '@element': 'GraphState_Property',
        'value': pin_value,
        'propertyKey': "locationPin{0:d}".format(pin_key)
    }
    pin_props.append(pin_prop)

# Replace the existing pin points by the list if pin points from the input file
report_content["json"]["sasReportState"]["visualElements"][0]["rendererStates"][0]["properties"] = pin_props

# Replace the report content by the updated content
update_report_content(
    content=report_content["json"],
    name=report_name,
    path=report_location,
    auth=auth_info)
print("Report '{0:s}' located in '{1:s}' has been updated!".format(
    report_name, report_location))
