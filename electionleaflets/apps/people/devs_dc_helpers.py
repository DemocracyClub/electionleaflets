import requests

from django.conf import settings

class DevsDCAPIHelper:
    def __init__(self):
        self.AUTH_TOKEN = settings.DEVS_DC_AUTH_TOKN
        self.base_url = "https://developers.democracyclub.org.uk/api/v1"

    def make_request(self, endpoint, **params):
        default_params = {
            "auth_token": self.AUTH_TOKEN
        }
        if params:
            default_params.update(params)
        url = "{}/{}/".format(self.base_url, endpoint)
        return requests.get(url, default_params)

    def postcode_request(self, postcode):
        return self.make_request("postcode/{}".format(postcode))
