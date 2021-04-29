import requests

from django.conf import settings
from django.core.cache import cache
from django.utils.cache import patch_response_headers

from constituencies.models import Constituency


def geocode(postcode):
    """
    Use MaPit to convert the postcode to a location and constituency
    """
    cache_key = postcode.replace(" ", "")
    cached = cache.get(cache_key)
    if cached:
        return cached
    try:
        url = "%s/postcode/%s" % (settings.MAPIT_API_URL, postcode)
        headers = {}
        if settings.MAPIT_API_KEY:
            headers["X-Api-Key"] = settings.MAPIT_API_KEY
        res = requests.get(url, headers=headers)
        res_json = res.json()
        if "code" in res_json and res_json["code"] == 404:
            return None
        else:
            constituency = Constituency.objects.get(
                constituency_id=str(res_json["shortcuts"]["WMC"])
            )
            lat = res_json["wgs84_lat"]
            lon = res_json["wgs84_lon"]

        result = {
            "wgs84_lon": lon,
            "wgs84_lat": lat,
            "constituency": constituency,
        }
    except Exception as e:
        print(e)
        result = None
    cache.set(cache_key, result, 60 * 60 * 60 * 24)
    return result


class CacheControlMixin(object):
    cache_timeout = 60

    def get_cache_timeout(self):
        return self.cache_timeout

    def dispatch(self, *args, **kwargs):
        response = super(CacheControlMixin, self).dispatch(*args, **kwargs)
        patch_response_headers(response, self.get_cache_timeout())
        return response
