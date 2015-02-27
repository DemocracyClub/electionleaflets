import requests

from constituencies.models import Constituency

import constants


def geocode(postcode):
    """
    Use MaPit to convert the postcode to a location and constituency
    """
    res = requests.get("%s/postcode/%s" % (constants.MAPIT_URL, postcode))
    res_json = res.json()
    constituency = Constituency.objects.get(
        constituency_id=str(res_json['shortcuts']['WMC']))
    return {
        'wgs84_lon': res_json['wgs84_lon'],
        'wgs84_lat': res_json['wgs84_lat'],
        'constituency': constituency,
    }
