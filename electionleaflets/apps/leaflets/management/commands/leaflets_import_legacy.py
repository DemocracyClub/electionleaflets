# -*- coding: utf-8 -*-
import os
import re

from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.files import File

from legacy.models import legacyLeaflet, legacyParty

from leaflets.models import Leaflet, LeafletImage
from constituencies.models import Constituency
from uk_political_parties.models import Party


class Command(BaseCommand):

    def clean_legacy_leaflet(self, legacy_leaflet, party=None, constituency=None):
        data = legacy_leaflet.__dict__.copy()
        del data['publisher_party_id']
        del data['_publisher_party_cache']
        del data['_state']
        del data['lng']
        del data['lat']
        data['publisher_party'] = party
        data['constituency'] = constituency
        if data.get('live'):
            data['status'] = 'live'
        else:
            data['status'] = 'removed'
        del data['live']
        return data

    def clean_legacy_leaflet_image(self, legacy_image):
        data = {}
        key = "%s.jpg" % legacy_image.image_key
        if getattr(settings, 'IMAGE_LOCAL_CACHE'):
            image_path = os.path.join(
                settings.IMAGE_LOCAL_CACHE,
                key
            )

            if os.path.exists(image_path):
                print("Exists")
                f = open(image_path, 'r')
                data['image'] = File(f)
            else:
                image_path = os.path.join(
                    settings.IMAGE_LOCAL_CACHE,
                    'large',
                    key
                )
                if os.path.exists(image_path):
                    print("Exists")
                    f = open(image_path, 'r')
                    data['image'] = File(f)
                else:
                    print("Doesn't exist")
            return data

    def clean_constituency(self, con):
        con_name = con.constituency.name
        if con_name == "Ynys Mon":
            con_name = "Ynys Môn"
        if con_name == "Cotswold":
            con_name = "The Cotswolds"
        if con_name == "Taunton":
            con_name = "Taunton Deane"
        try:
            con = Constituency.objects.get(name__iexact=con_name)
        except Constituency.DoesNotExist:
            con_name = ", ".join(con_name.split(' ', 1))
            con = Constituency.objects.get(name=con_name)
        return con

    def clean_postcode(self, postcode):
        try:
            postcode = postcode.encode("utf-8")
            postcode = postcode.upper()
            postcode = postcode.replace('!', "1")
            postcode = postcode.replace('@', "2")
            postcode = postcode.replace('"', "2")
            postcode = postcode.replace('£', "3")
            postcode = postcode.replace('$', "4")
            postcode = postcode.replace('%', "5")
            postcode = postcode.replace('^', "6")
            postcode = postcode.replace('&', "7")
            postcode = postcode.replace('*', "8")
            postcode = postcode.replace('(', "9")
            postcode = postcode.replace(')', "0")
            postcode = re.sub(r'[^\x00-\x7F]+', ' ', postcode)
            postcode = re.sub('^[A-Z0-9\s]', '', postcode)
            postcode = postcode.strip()
        except:
            import ipdb
            ipdb.set_trace()
        return postcode

    def handle(self, **options):
        for legacy_leaflet in legacyLeaflet.objects.all():
            if not legacy_leaflet.date_uploaded:
                if legacy_leaflet.date_delivered:
                    legacy_leaflet.date_uploaded = legacy_leaflet.date_delivered

            if legacy_leaflet.date_uploaded:
                if not bool(legacy_leaflet.publisher_party_id):
                    party = None
                else:
                    party = Party.objects.find_party_by_name(
                        legacy_leaflet.publisher_party.name)

                    cons = legacy_leaflet.legacyleafletconstituency_set.all()
                    con = None
                    if cons:
                        con = cons[0]
                        con = self.clean_constituency(con)

                    legacy_leaflet.postcode = self.clean_postcode(
                        legacy_leaflet.postcode)
                    new_leaflet, created = Leaflet.objects.update_or_create(
                        pk=legacy_leaflet.pk,
                        defaults=self.clean_legacy_leaflet(
                            legacy_leaflet,
                            party,
                            constituency=con
                        ))
                    print(new_leaflet.pk, end=' ')
                    if not new_leaflet.images.all():
                        print("Adding images")
                        for legacy_image in legacy_leaflet.images.all():
                            new_image, created = LeafletImage.objects.update_or_create(
                                leaflet=new_leaflet,
                                legacy_image_key=legacy_image.image_key,
                                defaults=self.clean_legacy_leaflet_image(legacy_image))
                    else:
                        print("")
