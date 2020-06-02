from ..Folders import find_object_in_folder
from ..call_rest import call_rest


def get_report(name, folder_id="", path="", auth={}):
    # Identify the report based on passed report information
    selected_report = find_object_in_folder(
        name,
        folder_id=folder_id,
        path=path,
        auth=auth)
    if selected_report["json"] != {}:
        report_uri = selected_report["json"]["uri"]
        endpoint = "{0:s}#standard".format(report_uri)
        headers = {
            'Accept': 'application/vnd.sas.report+json'
        }
        response = call_rest(
            endpoint,
            "get",
            headers=headers,
            auth=auth)
    else:
        response = {'json': {}}
    return response
