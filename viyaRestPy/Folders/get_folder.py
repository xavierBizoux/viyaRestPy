from ..call_rest import call_rest


def get_folder(path, auth={}):
    endpoint = "/folders/folders/@item"
    params = {"path": path}
    try:
        response = call_rest(
            endpoint,
            "get",
            params=params,
            auth=auth)
    except:
        response = {"json": {}}
    return response
