from .getReport import getReport
from ..callRest import callRest

def updateReportContent(content="", report={}, name="", path="", auth={}):
    if bool(report):
        endpoint = "/reports/reports/{0:s}/content".format(
            report["json"]["id"])
    else:
        report = getReport(name, path=path, auth=auth)
        if report != {}:
            endpoint = "/reports/reports/{0:s}/content".format(
            report["json"]["id"])
            data = content
            headers = {
                'Content-Type': 'application/vnd.sas.report.content+json',
                'If-Match': report["headers"]["ETag"]
            }
            callRest(endpoint, "put", data=data, headers=headers, auth=auth)