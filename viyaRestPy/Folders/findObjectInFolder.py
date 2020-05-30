import sys
from .getFolder import getFolder
from ..callRest import callRest


def findObjectInFolder(name, folderId="", path="", auth={}):
    selectedObject = {
        'json': {}
    }
    if folderId == "" and path == "":
        raise ValueError("You should provide a folderId or a path.")
    else:
        if folderId != "":
            endpoint = "/folders/folders/{0:s}/members".format(folderId)
        else:
            response = getFolder(path, auth=auth)
            if response['json'] != {}:
                folderId = response["json"]['id']
                endpoint = "/folders/folders/{0:s}/members".format(folderId)
            else:
                print("Folder '{0}' doesn't exist.".format(path))
                return selectedObject
    params = {"filter": 'contains(name,"' + name + '")'}
    try:
        response = callRest(
            endpoint,
            "get",
            params=params,
            auth=auth)
        selectedObject = {"json": response["json"]["items"][0]}
    except IndexError:
        print(
            "Object '{0:s}' could not be found at '{1:s}'.".format(name, path))
    return selectedObject
