from .get_report import get_report
from ..call_rest import call_rest


def delete_report(name="", path="", report_id="", auth={}):
    # Function to delete an existing report
    if report_id == "" and path == "" and name == "":
        raise ValueError(
            "You should provide a path and a name or the reportId.")
    else:
        if report_id != "":
            if "/reports/reports" in reportId:
                endpoint = "{0:s}".format(reportId)
            else:
                endpoint = "/reports/reports/{0:s}".format(report_id)
        else:
            if path == "" or name == "":
                raise ValueError(
                    "You should provide a path and a name for the report.")
            else:
                report = get_report(name, path=path, auth=auth)
                if report != {}:
                    endpoint = "/reports/reports/{0:s}".format(
                        report["json"]["id"])
                    headers = {
                        'Accept': '*/*'
                    }
                    try:
                        response = call_rest(
                            endpoint, "delete", headers=headers, auth=auth)
                        return response
                    except:
                        print(
                            "The report named '{0:s}' could not be deleted '{1:s}'.".format(name, path))
                    print("The report named '{0:s}' located in '{1:s}' has been deleted.".format(
                        name, path))
