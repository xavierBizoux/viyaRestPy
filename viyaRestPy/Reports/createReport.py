from .getReport import getReport
from .updateReportContent import updateReportContent
from ..Folders import getFolder
from ..callRest import callRest


def createReport(name="", path="", content="", auth={}):
    report = getReport(name=name, path=path, auth=auth)
    if report == {}:
        folder = getFolder(path, auth=auth)
        folderId = folder["json"]["links"][0]["uri"]
        endpoint = "/reports/reports"
        data = {"name": name,
                "description": name}
        params = {"parentFolderUri": folderId}
        headers = {
            'Content-Type': 'application/vnd.sas.report+json',
            'Accept': 'application/vnd.sas.report+json'
        }
        report = callRest(endpoint,
                          "post",
                          data=data,
                          params=params,
                          headers=headers,
                          auth=auth)
        print("The report named '{0:s}' has been created in '{1:s}'.".format(name, path))
        if bool(content):
            updateReportContent(
                content=content,
                report=report,
                auth=auth)
        return report
    else:
        print("A report named {0:s} already exists in {1:s}.".format(name, path))
        print("Please consider running updateReportContent function to update the existing report or delete the report.")

