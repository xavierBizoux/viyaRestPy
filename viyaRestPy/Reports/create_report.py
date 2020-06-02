from .get_report import get_report
from .update_report_content import update_report_content
from ..Folders import get_folder, create_folder
from ..call_rest import call_rest


def create_report(name="", path="", content="", auth={}):
    report = get_report(name=name, path=path, auth=auth)
    if report['json'] == {}:
        folder = get_folder(path, auth=auth)
        if folder["json"] == {}:
            folder = create_folder(path, auth=auth)
        folder_id = folder["json"]["links"][0]["uri"]
        endpoint = "/reports/reports"
        data = {"name": name,
                "description": name}
        params = {"parentFolderUri": folder_id}
        headers = {
            'Content-Type': 'application/vnd.sas.report+json',
            'Accept': 'application/vnd.sas.report+json'
        }
        report = call_rest(endpoint,
                          "post",
                          data=data,
                          params=params,
                          headers=headers,
                          auth=auth)
        print("The report named '{0:s}' has been created in '{1:s}'.".format(name, path))
        if bool(content):
            update_report_content(
                content=content,
                report=report,
                auth=auth)
        return report
    else:
        print("A report named {0:s} already exists in {1:s}.".format(name, path))
        print("Please consider running updateReportContent function to update the existing report or delete the report.")

