from .get_report import get_report
from ..call_rest import call_rest


def get_report_content(name="", path="", report_uri="", auth={}):
    # Define the endpoint based on passed report information
    if report_uri == "" and path == "" and name == "":
        raise ValueError(
            "You should provide a path and a name or the reportId.")
    else:
        if report_uri != "":
            if "/reports/reports" in report_uri:
                endpoint = "{0:s}/content".format(report_uri)
            else:
                endpoint = "/reports/reports/{0:s}/content".format(report_uri)
        else:
            if path == "" or name == "":
                raise ValueError(
                    "You should provide a path and a name for the report.")
            else:
                report = get_report(
                    name,
                    path=path,
                    auth=auth)
                if report != {}:
                    endpoint = "/reports/reports/{0:s}/content".format(
                        report["json"]["id"])
                    headers = {
                        'Accept': 'application/vnd.sas.report.content+json'
                    }
                    response = call_rest(
                        endpoint,
                        "get",
                        headers=headers,
                        auth=auth)
                    return response
