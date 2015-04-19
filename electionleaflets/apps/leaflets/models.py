import os
from cStringIO import StringIO

from sorl.thumbnail import ImageField
from sorl.thumbnail import delete
import pytesser
from PIL import Image

from django.db import models
from django.contrib.gis.db import models as geo_model
from django.contrib.gis.geos import Point
from django.core.files.base import ContentFile
from django.forms.models import model_to_dict

from core.helpers import geocode
from constituencies.models import Constituency
from people.models import Person
from elections.models import Election
from uk_political_parties.models import Party

import constants


class Leaflet(geo_model.Model):
    def __init__(self, *args, **kwargs):
        super(Leaflet, self).__init__(*args, **kwargs)
        self._initial = model_to_dict(self, fields=[field.name for field in
                             self._meta.fields])

    title = models.CharField(blank=True, max_length=765)
    description = models.TextField(blank=True, null=True)
    publisher_party = models.ForeignKey(Party, blank=True, null=True)
    publisher_person = models.ForeignKey(Person, blank=True, null=True)
    election = models.ForeignKey(Election, null=True)
    constituency = models.ForeignKey(Constituency, blank=True, null=True)
    imprint = models.TextField(blank=True, null=True)
    postcode = models.CharField(max_length=150, blank=True)
    location = geo_model.PointField(null=True, blank=True)
    name = models.CharField(blank=True, max_length=300)
    email = models.CharField(blank=True, max_length=300)
    date_uploaded = models.DateTimeField(auto_now_add=True)
    date_delivered = models.DateTimeField(blank=True, null=True)
    status = models.CharField(choices=constants.LEAFLET_STATUSES,
        null=True, blank=True, max_length=255)
    reviewed = models.BooleanField(default=False)

    objects = geo_model.GeoManager()

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ('-date_uploaded',)

    def get_absolute_url(self):
        from django.contrib.sites.models import Site
        return 'http://%s/leaflets/%s/' % (Site.objects.get_current().domain,
            self.id)

    def get_first_image(self):
        try:
            return self.images.all()[0]
        except IndexError:
            # TODO: Set image_key to value for 'empty' image
            return None

    def get_title(self):
        if self.title and len(self.title):
            return self.title
        elif self.publisher_party:
            return '%s leaflet' % self.publisher_party.party_name
        else:
            "Untitled leaflet"

    def geocode(self, postcode):
        data = geocode(postcode)
        if data:
            self.constituency = data['constituency']
            self.location = Point(
                data['wgs84_lon'],
                data['wgs84_lat'],
            )



    def save(self, *args, **kwargs):
        if self.postcode:
            if self.postcode != self._initial['postcode']:
                self.geocode(self.postcode)

        super(Leaflet, self).save(*args, **kwargs)


class LeafletImage(models.Model):
    leaflet = models.ForeignKey(Leaflet, related_name='images')
    image = ImageField(upload_to="leaflets", max_length=255)
    raw_image = ImageField(upload_to="raw_leaflets", blank=True, max_length=255)
    legacy_image_key = models.CharField(max_length=255, blank=True)
    image_type = models.CharField(choices=constants.IMAGE_TYPES,
        null=True, blank=True, max_length=255)
    image_text = models.TextField(blank=True)

    class Meta:
        ordering = ['image_type']

    def save(self, *args, **kwargs):
        """
        Save a copy of the raw_image as soon as possible.

        This is so we don't destroy images, by cropping them too small
        for example.
        """
        super(LeafletImage, self).save(*args, **kwargs)
        if not self.raw_image:
            self.raw_image.save(self.image.name, self.image.file)
        self._clean_image()

    def _clean_image(self):
        from sorl.thumbnail.engines.pil_engine import Engine
        from sorl.thumbnail.images import ImageFile

        e = Engine()
        f = ImageFile(self.image.file)
        tmp_image = e.get_image(f)
        tmp_image = e._orientation(tmp_image)
        new_file = StringIO()
        tmp_image.save(new_file, 'jpeg')
        file_content = ContentFile(new_file.getvalue())
        self.image.save(self.image.name, file_content, save=False)

    @models.permalink
    def get_absolute_url(self):
        return ('full_image', (), {'pk': self.pk})

    @property
    def dimensions(self):
        im = Image.open(self.image.path)
        return im.size

    def crop(self, x=None, y=None, x2=None, y2=None):
        if not all((x, y, x2, y2)):
            raise ValueError('All points are required')
        file_name = self.raw_image.name
        im = Image.open(self.raw_image.file)
        cropped = im.copy()
        cropped = cropped.crop((x, y, x2, y2))
        new_file = StringIO()
        cropped.save(new_file, 'jpeg')
        file_content = ContentFile(new_file.getvalue())
        self.image.save(file_name, file_content)
        delete(self.image, delete_file=False)

    def rotate(self, rotate_angle):
        """
        Make sure we rotate both images.
        """
        if not self.raw_image:
            self.raw_image = self.image
            self.raw_image.save()
        for image_field in (
            # self.raw_image,
            self.image,
            ):
            file_name = image_field.name
            im = Image.open(image_field.file)
            rotated = im.copy()
            rotated = rotated.rotate(rotate_angle)
            new_file = StringIO()
            rotated.save(new_file, 'jpeg')
            file_content = ContentFile(new_file.getvalue())
            image_field.save(file_name, file_content)
            delete(self.image, delete_file=False)

    def ocr(self):
        if not self.image:
            return ""

        image_path = self.image.path

        text = pytesser.image_to_string(image_path)
        text = os.linesep.join([s for s in text.splitlines() if s])
        self.image_text = text
        self.save()
        os.remove(image_path)
        return text
