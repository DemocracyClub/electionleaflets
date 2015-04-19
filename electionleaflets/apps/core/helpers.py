import requests

from django.core.cache import cache

from constituencies.models import Constituency

import constants


def geocode(postcode):
    """
    Use MaPit to convert the postcode to a location and constituency
    """
    cached = cache.get(postcode)
    if cached:
        return cached
    try:
        res = requests.get("%s/postcode/%s" % (constants.MAPIT_URL, postcode))
        res_json = res.json()
        constituency = Constituency.objects.get(
            constituency_id=str(res_json['shortcuts']['WMC']))
        result = {
            'wgs84_lon': res_json['wgs84_lon'],
            'wgs84_lat': res_json['wgs84_lat'],
            'constituency': constituency,
        }
    except Exception, e:
        result = None
    cache.set(postcode, result, 60*60*60*24)
    return result