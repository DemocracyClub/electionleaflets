import requests

from django.conf import settings


class DevsDCAPIHelper:
    def __init__(self):
        self.AUTH_TOKEN = settings.DEVS_DC_AUTH_TOKEN
        self.base_url = "https://developers.democracyclub.org.uk/api/v1"
        self.ballot_cache = {}

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

    def ballot_request(self, ballot_paper_id):
        if ballot_paper_id not in self.ballot_cache:
            r = self.make_request("elections/{}".format(ballot_paper_id))
            if r.status_code == 200:
                self.ballot_cache[ballot_paper_id] = r
            else:
                return r

        return self.ballot_cache[ballot_paper_id]
