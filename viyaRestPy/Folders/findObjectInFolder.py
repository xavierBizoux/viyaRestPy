import sys
from .getFolder import getFolder
from ..callRest import callRest


def findObjectInFolder(name, folderId="", path="", auth={}):
    # Define the
    if folderId == "" and path == "":
        raise ValueError("You should provide a folderId or a path.")
    else:
        if folderId != "":
            endpoint = "/folders/folders/{0:s}/members".format(folderId)
        else:
            folder = getFolder(path, auth=auth)
            folderId = folder["json"]["id"]
            endpoint = "/folders/folders/{0:s}/members".format(folderId)
    params = {"filter": 'contains(name,"' + name + '")'}
    response = callRest(
        endpoint,
        "get",
        params=params,
        auth=auth)
    try:
        selectedObject = {"json": response["json"]["items"][0]}
    except IndexError:
        print(
            "Object '{0:s}' could not be found at '{1:s}'.".format(name, path))
        selectedObject = {"json": ""}
    return selectedObject