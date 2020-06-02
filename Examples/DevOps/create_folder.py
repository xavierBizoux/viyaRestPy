#!/usr/local/bin/python3
#
# create_folder.py
# Xavier Bizoux, GEL
# May 2020
#
# Create folder recursively
#
# Change History
#
# sbxxab 30MAY2020
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
#### ./create_folder.py     -u myAdmin                          ####
####                        -p myAdminPW                        ####
####                        -sn http://myServer.sas.com:80      ####
####                        -an app                             ####
####                        -as appsecret                       ####
####                        -f "/Users/sbxxab/My Folder"        ####
####################################################################
# Import modules
import json
import argparse
import sys
from viyaRestPy.Folders import create_folder

# Define arguments for command line execution
parser = argparse.ArgumentParser(
    description="Create folders recursively")
parser.add_argument("-f",
                    "--folder",
                    help="Folder to be created",
                    required=False)
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
path = args.folder

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

create_folder(path, auth=auth_info)
