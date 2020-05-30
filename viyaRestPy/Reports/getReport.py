from ..Folders import findObjectInFolder
from ..callRest import callRest

def getReport(name, folderId="", path="", auth={}):
    # Identify the report based on passed report information
    selectedReport = findObjectInFolder(
        name, folderId=folderId, path=path, auth=auth)
    if selectedReport["json"] != {} :
        reportUri = selectedReport["json"]["uri"]
        endpoint = "{0:s}#standard".format(reportUri)
        headers = {
            'Accept': 'application/vnd.sas.report+json'
        }
        response = callRest(
            endpoint,
            "get",
            headers=headers,
            auth=auth)
    else:
        response = {'json': {}}
    return response