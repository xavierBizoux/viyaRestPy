from .getReport import getReport
from ..callRest import callRest

def getReportContent(name="", path="", reportUri="", auth={}):
    # Define the endpoint based on passed report information
    if reportUri == "" and path == "" and name == "":
        raise ValueError(
            "You should provide a path and a name or the reportId.")
    else:
        if reportUri != "":
            if "/reports/reports" in reportUri:
                endpoint = "{0:s}/content".format(reportUri)
            else:
                endpoint = "/reports/reports/{0:s}/content".format(reportUri)
        else:
            if path == "" or name == "":
                raise ValueError(
                    "You should provide a path and a name for the report.")
                # sys.exit()
            else:
                report = getReport(
                    name,
                    path=path,
                    auth=auth)
                if report != {}:
                    endpoint = "/reports/reports/{0:s}/content".format(
                        report["json"]["id"])
                    headers = {
                        'Accept': 'application/vnd.sas.report.content+json'
                    }
                    response = callRest(
                        endpoint,
                        "get",
                        headers=headers,
                        auth=auth)
                    return response