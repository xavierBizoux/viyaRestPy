#!/usr/local/bin/python3
#
# lodPinPoints.py
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
#### ./loadPinPoints.py     -u myAdmin                          ####
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
from viyaRestPy.Reports import getReportContent, getReport, updateReportContent

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
reportLocation = args.reportlocation
reportName = args.reportname
backupFolder = args.backupFolder
inFile = args.inputFile

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

# Extract the content of the existing report
reportContent = getReportContent(
    name=reportName,
    path=reportLocation,
    auth=authInfo)

# Create a backup file of the report
# Create a JSON representation of the report
data = {"name": reportName, "location": reportLocation,
        "content": reportContent["json"]}

# Generate output file
outFile = backupFolder + reportName + ".json"
with open(outFile, "w") as out:
    json.dump(data, out)


# Read pin point information
with open(inFile, newline='') as inputFile:
    reader = csv.reader(inputFile)
    pinData = list(reader)
    pinData.remove(pinData[0])


# Transform the pin points data to VA report usable information
pinProps = []
for pinKey, pinPoint in enumerate(pinData):
    pinValue = 'Name="{0:s}" Address="{1:s}, {2:s}, {3:s}" LatLon={4:s},{5:s} Type=CUSTOM OriginType=CUSTOM VisualState=DISPLAYED Color=2919126 SelectionMode=NONE IsSelected=true'.format(
        pinPoint[0], pinPoint[5], pinPoint[4], pinPoint[3], pinPoint[2], pinPoint[1])
    pinProp = {
        '@element': 'GraphState_Property',
        'value': pinValue,
        'propertyKey': "locationPin{0:d}".format(pinKey)
    }
    pinProps.append(pinProp)

# Replace the existing pin points by the list if pin points from the input file
reportContent["json"]["sasReportState"]["visualElements"][0]["rendererStates"][0]["properties"] = pinProps
print(reportContent["json"])
# Replace the report content by the updated content
updateReportContent(
    content=reportContent["json"],
    name=reportName,
    path=reportLocation,
    auth=authInfo)
print("Report '{0:s}' located in '{1:s}' has been updated!".format(
    reportName, reportLocation))
