import sys
from .get_report import get_report
from ..call_rest import call_rest

def update_report_content(content="", report={}, name="", path="", auth={}):
    if bool(report):
        endpoint = "/reports/reports/{0:s}/content".format(
            report["json"]["id"])
    else:
        report = get_report(name, path=path, auth=auth)
        if report["json"] != {}:
            endpoint = "/reports/reports/{0:s}/content".format(
            report["json"]["id"])
        else:
            sys.exit()
    data = content
    headers = {
        'Content-Type': 'application/vnd.sas.report.content+json',
        'If-Match': report["headers"]["ETag"]
    }
    call_rest(endpoint, "put", data=data, headers=headers, auth=auth)