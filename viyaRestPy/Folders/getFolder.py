from ..callRest import callRest


def getFolder(path, auth={}):
    endpoint = "/folders/folders/@item"
    params = {"path": path}
    try:
        response = callRest(
            endpoint,
            "get",
            params=params,
            auth=auth)
    except:
        response = {"json": {}}
    return response
