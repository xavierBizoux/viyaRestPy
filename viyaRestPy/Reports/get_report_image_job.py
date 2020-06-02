from ..call_rest import call_rest


def get_report_image_job(job_id, auth={}):
    endpoint = "/reportImages/jobs/{0:s}".format(job_id)
    params = {
        "wait": 5
    }
    headers = {
        'Accept': 'application/vnd.sas.report.images.job+json'
    }
    response = call_rest(endpoint,
                        "get",
                        params=params,
                        headers=headers,
                        auth=auth)
    return response
