import sys
from .get_folder import get_folder
from ..call_rest import call_rest


def find_object_in_folder(name, folder_id="", path="", auth={}):
    selected_object = {
        'json': {}
    }
    if folder_id == "" and path == "":
        raise ValueError("You should provide a folderId or a path.")
    else:
        if folder_id != "":
            endpoint = "/folders/folders/{0:s}/members".format(folder_id)
        else:
            response = get_folder(path, auth=auth)
            if response['json'] != {}:
                folder_id = response["json"]['id']
                endpoint = "/folders/folders/{0:s}/members".format(folder_id)
            else:
                print("Folder '{0}' doesn't exist.".format(path))
                return selected_object
    params = {"filter": 'contains(name,"' + name + '")'}
    try:
        response = call_rest(
            endpoint,
            "get",
            params=params,
            auth=auth)
        selected_object = {"json": response["json"]["items"][0]}
    except IndexError:
        print(
            "Object '{0:s}' could not be found at '{1:s}'.".format(name, path))
    return selected_object
