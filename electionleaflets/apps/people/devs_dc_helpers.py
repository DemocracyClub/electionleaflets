import requests

from django.conf import settings


class DevsDCAPIHelper:
    def __init__(self):
        self.AUTH_TOKEN = settings.DEVS_DC_AUTH_TOKEN
        self.base_url = "https://developers.democracyclub.org.uk/api/v1"
        self.ballot_cache = {}

    def make_request(self, endpoint, **params):
        default_params = {"auth_token": self.AUTH_TOKEN}
        if params:
            default_params.update(params)
        url = "{}/{}/".format(self.base_url, endpoint)
        return requests.get(url, default_params)

    def postcode_request(self, postcode):
        """
        In some cases a postcode can reques an address picker.

        As a hack, because we don't really want the actual address, we just pick
        the first address whenever we see one. This will cause some errors some
        times, but not enough for us to worry about at the moment.

        """
        req = self.make_request(f"postcode/{postcode}")
        if req.json()["address_picker"] == True:
            # This postcode is split, just grab the first address and use that.
            uprn = req.json()["addresses"][0]["slug"]
            return self.make_request(f"address/{uprn}")
        return req


    def ballot_request(self, ballot_paper_id):
        if ballot_paper_id not in self.ballot_cache:
            r = self.make_request("elections/{}".format(ballot_paper_id))
            if r.status_code == 200:
                self.ballot_cache[ballot_paper_id] = r
            else:
                return r

        return self.ballot_cache[ballot_paper_id]
