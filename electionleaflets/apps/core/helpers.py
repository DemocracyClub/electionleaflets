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
        if 'code' in res_json and res_json['code'] == 404:
            return None
        if 'code' in res_json and res_json['code'] == 400:
            # This might be an outcode, try to get that
            res = requests.get("%s/postcode/partial/%s" % (
                constants.MAPIT_URL, postcode))
            res_json = res.json()
            lat = res_json['wgs84_lat']
            lon = res_json['wgs84_lon']

            # Now get the point
            res = requests.get("%s/point/4326/%s,%s" % (
                constants.MAPIT_URL,
                res_json['wgs84_lon'],
                res_json['wgs84_lat'],
                ))
            res_json = res.json()

            # Now get the WMC
            WMC = {}
            for area in res_json:
                if area['type'] == 'WMC':
                    WMC = area

            constituency = Constituency.objects.get(
                constituency_id=str(WMC.get('id')))
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
    except Exception, e:
        print e
        result = None
    cache.set(postcode, result, 60*60*60*24)
    return result