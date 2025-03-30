import json
import time
from urllib.parse import urljoin, urlparse

import requests
from django.conf import settings
from django.forms import Textarea
from django.utils.cache import add_never_cache_headers, patch_response_headers
from requests.adapters import HTTPAdapter
from urllib3 import Retry

session = requests.Session()

retries = Retry(
    total=1,
    connect=1,
    backoff_factor=0.1,
    status_forcelist=[502, 503, 504],
    allowed_methods={"GET"},
)

session.mount(
    f"{urlparse(settings.YNR_BASE_URL).scheme}://",
    HTTPAdapter(max_retries=retries),
)


class CacheControlMixin(object):
    cache_timeout = 60

    def get_cache_timeout(self):
        return self.cache_timeout

    def dispatch(self, *args, **kwargs):
        response = super(CacheControlMixin, self).dispatch(*args, **kwargs)
        if settings.DEBUG:
            add_never_cache_headers(response)
            return response

        patch_response_headers(response, self.get_cache_timeout())
        return response


class YNRAPIHelper:
    def __init__(self, api_key=None):
        self.YNR_BASE = settings.YNR_BASE_URL
        self.API_KEY = api_key or settings.YNR_API_KEY  # handy for mocking URLs

        if not self.API_KEY:
            print(
                "WARNING: settings.YNR_API_KEY not set. Requests will be rate limited"
            )

    def get(self, endpoint, params=None, version="next", json=True):
        if not self.API_KEY:
            time.sleep(6)
        path = f"api/{version}/{endpoint}"
        url = urljoin(self.YNR_BASE, path)
        params = params or {}
        params["auth_token"] = self.API_KEY
        resp = session.get(url, params=params)
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
