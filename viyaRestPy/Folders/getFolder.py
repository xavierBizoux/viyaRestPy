from ..callRest import callRest

def getFolder(path, auth={}):
    endpoint = "/folders/folders/@item"
    params = {"path": path}
    folder = callRest(
        endpoint,
        "get",
        params=params,
        auth=auth)
    return folder