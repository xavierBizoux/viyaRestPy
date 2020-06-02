from ..call_rest import call_rest
from .get_folder import get_folder


def create_folder(path, auth={}):
    headers = {
        'Content-Type': 'application/vnd.sas.content.folder+json',
        'Accept': 'application/vnd.sas.content.folder+json'
    }
    folder_structure = path.split("/")
    folder_structure.pop(0)
    current_level = ""
    for folder_name in folder_structure:
        parent_level = current_level
        current_level = '/'.join([current_level, folder_name])
        data = {
            "name": folder_name,
            "type": "folder"
        }
        folder = get_folder(current_level, auth=auth)
        if folder['json'] == {}:
            print("Folder '{0}' doesn't exist. Creating it!".format(current_level))
            parent_folder = get_folder(parent_level, auth=auth)
            endpoint = "/folders/folders"
            params = {"parentFolderUri": "/folders/folders/{0}".format(parent_folder["json"]["id"])}
            call_rest(
                endpoint,
                "post",
                params=params,
                auth=auth,
                headers=headers,
                data=data)
            folder = get_folder(current_level, auth=auth)
    return folder
