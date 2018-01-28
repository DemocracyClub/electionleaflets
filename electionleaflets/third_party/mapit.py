"""
Performs a lookup of postcode to Lat/Lon using the mapit.mysociety.org API.
"""


def postcode_to_latlong(postcode):
    import urllib.request
    import urllib.error
    import urllib.parse
    from django.utils import simplejson as json

    url = 'https://mapit.mysociety.org/postcode/%s' % postcode.lower().replace(' ', '')
    result_dict = None
    try:
        request = urllib.request.urlopen(url)
        result_dict = json.load(request)
    except:
        pass

    if not result_dict or 'error' in result_dict:
        return None, None

    return result_dict['wgs84_lat'], result_dict['wgs84_lon']
