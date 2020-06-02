import json
import sys
from .get_report import get_report
from .get_report_image_job import get_report_image_job
from ..call_rest import call_rest


def get_report_image(name="", path="", auth={}):
    # Function to retrieve an image from the report
    report = get_report(name, path=path, auth=auth)
    endpoint = "/reportImages/jobs#requestsParams"
    if report["json"] != {}:
        data = {
            "reportUri": "/reports/reports/{0:s}".format(report["json"]["id"]),
            "size": "600x600",
            "layoutType": "entireSection",
            "wait": 5,
            "refresh": True
        }
    else:
        sys.exit()
    headers = {
        'Accept': 'application/vnd.sas.report.images.job+json'
    }
    job = call_rest(endpoint, 'post', data=data, headers=headers, auth=auth)
    job_data = job["json"]
    if job_data["state"] not in ["completed", "error"]:
        while job_data["state"] == "running":
            job = get_report_image_job(job_data['id'], auth=auth)
            job_data = job["json"]
    return job
