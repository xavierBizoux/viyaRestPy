from ..callRest import callRest
from .getFolder import getFolder


def createFolder(path, auth={}):
    headers = {
        'Content-Type': 'application/vnd.sas.content.folder+json',
        'Accept': 'application/vnd.sas.content.folder+json'
    }
    folderStructure = path.split("/")
    folderStructure.pop(0)
    currentLevel = ""
    for folderName in folderStructure:
        parentLevel = currentLevel
        currentLevel = '/'.join([currentLevel, folderName])
        data = {
            "name": folderName,
            "type": "folder"
        }
        folder = getFolder(currentLevel, auth=auth)
        if folder['json'] == {}:
            print("Folder '{0}' doesn't exist. Creating it!".format(currentLevel))
            parentFolder = getFolder(parentLevel, auth=auth)
            endpoint = "/folders/folders"
            params = {"parentFolderUri": "/folders/folders/{0}".format(parentFolder["json"]["id"])}
            callRest(
                endpoint,
                "post",
                params=params,
                auth=auth,
                headers=headers,
                data=data)
            folder = getFolder(currentLevel, auth=auth)
    return folder
