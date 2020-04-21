from .getReport import getReport
from ..callRest import callRest

def deleteReport(name="", path="", reportId="", auth={}):
    # Function to delete an existing report
    if reportId == "" and path == "" and name == "":
        raise ValueError(
            "You should provide a path and a name or the reportId.")
    else:
        if reportId != "":
            if "/reports/reports" in reportId:
                endpoint = "{0:s}".format(reportId)
            else:
                endpoint = "/reports/reports/{0:s}".format(reportId)
        else:
            if path == "" or name == "":
                raise ValueError(
                    "You should provide a path and a name for the report.")
            else:
                report = getReport(name, path=path, auth=auth)
                if report != {}:
                    endpoint = "/reports/reports/{0:s}".format(
                        report["json"]["id"])
                    headers = {
                        'Accept': '*/*'
                    }
                    try:
                        callRest(endpoint, "delete", headers=headers, auth=auth)
                    except:
                        print("The report named '{0:s}' could not be deleted '{1:s}'.".format(name, path))
                    print("The report named '{0:s}' located in '{1:s}' has been deleted.".format(name, path))