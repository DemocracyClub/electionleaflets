from django.http import HttpResponse
from django.contrib.sites.models import Site
from django.utils.html import escape

from leaflets.models import Leaflet, LeafletImage
from constituencies.models import Constituency
from uk_political_parties.models import Party

from rest_framework import viewsets

from .serializers import (ConstituencySerializer, PartySerializer,
    LeafletSerializer, LeafletImageSerializer)


class ConstituencyViewSet(viewsets.ModelViewSet):
    queryset = Constituency.objects.all()
    serializer_class = ConstituencySerializer


class PartyViewSet(viewsets.ModelViewSet):
    queryset = Party.objects.all()
    serializer_class = PartySerializer


class LeafletImageViewSet(viewsets.ModelViewSet):
    queryset = LeafletImage.objects.all()
    serializer_class = LeafletImageSerializer


class LeafletViewSet(viewsets.ModelViewSet):
    queryset = Leaflet.objects.all()
    serializer_class = LeafletSerializer

def latest(request, format):
    # TODO: Fix this to work properly
    from leaflets.models import Leaflet

    domain = Site.objects.get_current().domain

    leaflets = Leaflet.objects.order_by('-id').all()[0:20]
    resp = []
    for leaflet in leaflets:
        d = {}
        if leaflet.constituency_id:
            d['constituency'] = leaflet.constituency.name
        else:
            d['constituency'] = 'Unknown'
        d['constituency'] = str(d['constituency'])
        d['uploaded_date'] = str(leaflet.date_uploaded)
        d['delivery_date'] = str(leaflet.date_delivered)
        d['title'] = escape(leaflet.title)
        d['description'] = escape(leaflet.description)
        if leaflet.publisher_party_id:
            d['party'] = escape(leaflet.publisher_party.party_name)
        else:
            d['party'] =  "Unknown"
        i = leaflet.get_first_image()
        d['image'] = i.image.url
        d['link'] = leaflet.get_absolute_url()
        resp.append( d )

    output = '<?xml version="1.0" ?>\n'
    output += "<leaflets>"
    for d in resp:
        output += "<leaflet>"
        for k,v in d.iteritems():
            output += "<" + k + ">"
            output += v
            output += "</" + k + ">"
        output += "</leaflet>"

    output += "</leaflets>"
    return HttpResponse(output, content_type='text/xml')