# -*- coding: utf-8 -*-
import csv

from django.core.management.base import BaseCommand
from django.utils.encoding import force_text
from leaflets.models import LeafletImage


class Command(BaseCommand):
    def handle(self, **options):
        fieldnames = [
            "image_id",
            "raw_image_path",
            "image_path",
            "image_type",
            "image_text",
            "title",
            "description",
            "publisher_party_id",
            "publisher_party_name",
            "publisher_person_name",
            "publisher_person_remote_id",
            "election",
            "constituency",
            "imprint",
            "postcode",
            "location",
            "name",
            "email",
            "date_uploaded",
            "date_delivered",
            "status",
            "reviewed",
        ]
        with open("/tmp/meta_data.csv", "w") as csvfile:
            out = csv.DictWriter(csvfile, fieldnames=fieldnames)
        out.writeheader()
        for image in LeafletImage.objects.all():
            data = {
                "image_id": image.pk,
                "raw_image_path": image.raw_image.name,
                "image_path": image.image.name,
                "image_type": image.image_type,
                "title": image.leaflet.title,
                "image_text": image.image_text,
                "description": image.leaflet.description,
                "constituency": image.leaflet.constituency,
                "imprint": image.leaflet.imprint,
                "postcode": image.leaflet.postcode,
                "location": image.leaflet.location,
                "name": image.leaflet.name,
                "email": image.leaflet.email,
                "date_uploaded": image.leaflet.date_uploaded,
                "date_delivered": image.leaflet.date_delivered,
                "status": image.leaflet.status,
                "reviewed": image.leaflet.reviewed,
            }

            if image.leaflet.publisher_party:
                data.update(
                    {
                        "publisher_party_id": image.leaflet.publisher_party.pk,
                        "publisher_party_name": image.leaflet.publisher_party.party_name,
                    }
                )

            if image.leaflet.publisher_person:
                data.update(
                    {
                        "publisher_person_name": image.leaflet.publisher_person.name,
                        "publisher_person_remote_id": image.leaflet.publisher_person.remote_id,
                    }
                )
            if image.leaflet.election:
                data.update(
                    {
                        "election": image.leaflet.election,
                    }
                )

            for k, v in list(data.items()):
                data[k] = force_text(v, "utf8")
            out.writerow({k: v.encode("utf8") for k, v in list(data.items())})
