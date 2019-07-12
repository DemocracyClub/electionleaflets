import requests

from django.core.cache import cache

from constituencies.models import Constituency

from . import constants


def geocode(postcode):
    """
    Use MaPit to convert the postcode to a location and constituency
    """
    cache_key = postcode.replace(' ', '')
    cached = cache.get(cache_key)
    if cached:
        return cached
    try:
        res = requests.get("%s/postcode/%s" % (constants.MAPIT_URL, postcode), verify=False)
        res_json = res.json()
        if 'code' in res_json and res_json['code'] == 404:
            return None
        else:
            constituency = Constituency.objects.get(
                constituency_id=str(res_json['shortcuts']['WMC']))
            lat = res_json['wgs84_lat']
            lon = res_json['wgs84_lon']

        result = {
            'wgs84_lon': lon,
            'wgs84_lat': lat,
            'constituency': constituency,
        }
    except Exception as e:
        print(e)
        result = None
    cache.set(cache_key, result, 60 * 60 * 60 * 24)
    return result
