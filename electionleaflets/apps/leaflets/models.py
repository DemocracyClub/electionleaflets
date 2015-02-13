import os
from cStringIO import StringIO

from sorl.thumbnail import ImageField
import pytesser
from PIL import Image

from django.db import models
from django.core.files.base import ContentFile

from tags.models import Tag
from categories.models import Category
from constituencies.models import Constituency
from uk_political_parties.models import Party

import constants

class Leaflet(models.Model):
    title = models.CharField(blank=True, max_length=765)
    description = models.TextField(blank=True, null=True)
    publisher_party = models.ForeignKey(Party, blank=True, null=True)
    constituency = models.ForeignKey(Constituency, blank=True, null=True)

    attacks = models.ManyToManyField(Party, related_name='attacks',
        null=True, blank=True)
    tags = models.ManyToManyField(Tag, through='LeafletTag')
    categories = models.ManyToManyField(Category, through='LeafletCategory')
    imprint = models.TextField(blank=True, null=True)
    postcode = models.CharField(max_length=150, blank=True)
    lng = models.FloatField(blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    name = models.CharField(blank=True, max_length=300)
    email = models.CharField(blank=True, max_length=300)
    date_uploaded = models.DateTimeField(auto_now_add=True)
    date_delivered = models.DateTimeField(blank=True, null=True)
    status = models.CharField(choices=constants.LEAFLET_STATUSES,
        null=True, blank=True, max_length=255)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ('date_uploaded',)

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
            return '%s leaflet' % self.party.name
        else:
            "Untitled leaflet"


class LeafletImage(models.Model):
    leaflet = models.ForeignKey(Leaflet, related_name='images')
    image = ImageField(upload_to="leaflets")
    raw_image = ImageField(upload_to="raw_leaflets", blank=True)
    legacy_image_key = models.CharField(max_length=255, blank=True)
    image_type =  models.CharField(choices=constants.IMAGE_TYPES,
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

        file_name = self.image.name
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
        file_name = self.image.name
        im = Image.open(self.image.file)
        cropped = im.copy()
        cropped = cropped.crop((x,y,x2,y2))
        new_file = StringIO()
        cropped.save(new_file, 'jpeg')
        file_content = ContentFile(new_file.getvalue())
        self.image.save(file_name, file_content)


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


class LeafletCategory(models.Model):
    leaflet = models.ForeignKey(Leaflet)
    category = models.ForeignKey(Category)


class LeafletTag(models.Model):
    leaflet = models.ForeignKey(Leaflet)
    tag = models.ForeignKey(Tag)

    def __unicode__(self):
        return u'tagged %s' % (self.tag.tag,)


class Promise(models.Model):
    promise_id = models.IntegerField(primary_key=True)
    leaflet_id = models.IntegerField()
    detail = models.TextField()


class RateInteresting(models.Model):
    rate_interesting_id = models.IntegerField(primary_key=True)
    leaflet_id = models.IntegerField()
    description = models.TextField()
    user_name = models.CharField(max_length=765)
    user_email = models.CharField(max_length=765)


class RateInterestingSeq(models.Model):
    sequence = models.IntegerField(primary_key=True)


class RateType(models.Model):
    rate_type_id = models.IntegerField(primary_key=True)
    left_label = models.CharField(max_length=150)
    right_label = models.CharField(max_length=150, blank=True)


class RateValue(models.Model):
    rate_value_id = models.IntegerField(primary_key=True)
    leaflet_id = models.IntegerField()
    user_name = models.CharField(max_length=300)
    user_email = models.CharField(max_length=300)
    rate_type_id = models.IntegerField()
    value = models.IntegerField()


class RateValueSeq(models.Model):
    sequence = models.IntegerField(primary_key=True)
