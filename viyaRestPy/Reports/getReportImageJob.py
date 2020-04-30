from ..callRest import callRest


def getReportImageJob(jobId, auth={}):
    endpoint = "/reportImages/jobs/{0:s}".format(jobId)
    params = {
        "wait": 10
    }
    headers = {
        'Accept': 'application/vnd.sas.report.images.job+json'
    }
    response = callRest(endpoint,
                        "get",
                        params=params,
                        headers=headers,
                        auth=auth)
    return response
