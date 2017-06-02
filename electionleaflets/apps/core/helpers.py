from raven.contrib.django.raven_compat.models import client
import requests

from django.conf import settings
from django.core.cache import cache

from constituencies.models import Constituency


def geocode(postcode):
    """
    Use MaPit to convert the postcode to a location and constituency
    """
    cached = cache.get(postcode)
    if cached:
        return cached
    try:
        url = "%s/postcode/%s" % (settings.MAPIT_API_URL, postcode)
        headers = {}
        if settings.MAPIT_API_KEY:
            headers['X-Api-Key'] = settings.MAPIT_API_KEY
        res = requests.get(url, verify=False, headers=headers)
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
        client.captureException()
        result = None

    cache.set(postcode, result, 60*60*60*24)
    return result
