import json
from .getReport import getReport
from .getReportImageJob import getReportImageJob
from ..callRest import callRest


def getReportImage(name="", path="", auth={}):
    # Function to retrieve an image from the report
    report = getReport(name, path=path, auth=auth)
    endpoint = "/reportImages/jobs#requestsParams"
    data = {
        "reportUri": "/reports/reports/{0:s}".format(report["json"]["id"]),
        "size": "600x600",
        "layoutType": "entireSection",
        "wait": 5,
        "refresh": True
    }
    headers = {
        'Accept': 'application/vnd.sas.report.images.job+json'
    }
    job = callRest(endpoint, 'post', data=data, headers=headers, auth=auth)
    jobData = job["json"]
    if jobData["state"] not in ["completed", "error"]:
        while jobData["state"] == "running":
            job = getReportImageJob(jobData['id'], auth=auth)
            jobData = job["json"]
    return job
