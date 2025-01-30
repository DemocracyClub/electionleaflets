import json
from urllib.parse import urljoin

import requests
from django.conf import settings
from django.forms import Textarea
from django.utils.cache import patch_response_headers


class CacheControlMixin(object):
    cache_timeout = 60

    def get_cache_timeout(self):
        return self.cache_timeout

    def dispatch(self, *args, **kwargs):
        response = super(CacheControlMixin, self).dispatch(*args, **kwargs)
        patch_response_headers(response, self.get_cache_timeout())
        return response


class YNRAPIHelper:
    def __init__(self, api_key=None):
        self.YNR_BASE = settings.YNR_BASE_URL
        self.API_KEY = api_key or settings.YNR_API_KEY  # handy for mocking URLs

    def get(self, endpoint, params=None, version="next", json=True):
        path = f"api/{version}/{endpoint}"
        url = urljoin(self.YNR_BASE, path)
        params = params or {}
        params["auth_token"] = self.API_KEY
        resp = requests.get(url, params=params)
        resp.raise_for_status()

        if json:
            return resp.json()
        return resp


class JSONEditor(Textarea):
    def render(self, name, value, attrs=None, renderer=None):
        # if its valid json, pretty print it
        # if not (e.g: on init, validation error)
        # just use the input string
        try:
            value = json.dumps(json.loads(value), sort_keys=True, indent=4)
        finally:
            return super().render(name, value, attrs)
