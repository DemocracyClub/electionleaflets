from io import BytesIO
import re

from django.urls import reverse
from sorl.thumbnail import ImageField
from sorl.thumbnail import delete
import piexif
from PIL import Image

from django.db import models
from django.core.files.base import ContentFile
from django.forms.models import model_to_dict

from core.helpers import geocode
from constituencies.models import Constituency
from people.devs_dc_helpers import DevsDCAPIHelper
from people.models import Person
from elections.models import Election
from uk_political_parties.models import Party

from . import constants

devs_dc_helper = DevsDCAPIHelper()


class Leaflet(models.Model):
    def __init__(self, *args, **kwargs):
        super(Leaflet, self).__init__(*args, **kwargs)
        self._initial = model_to_dict(
            self, fields=[field.name for field in self._meta.fields]
        )

    title = models.CharField(blank=True, max_length=765)
    description = models.TextField(blank=True, null=True)
    publisher_party = models.ForeignKey(
        Party, blank=True, null=True, on_delete=models.CASCADE
    )
    ynr_party_id = models.CharField(
        blank=True, null=True, max_length=255, db_index=True
    )
    ynr_party_name = models.CharField(blank=True, null=True, max_length=255)
    publisher_person = models.ForeignKey(
        Person, blank=True, null=True, on_delete=models.CASCADE
    )
    ynr_person_id = models.IntegerField(blank=True, null=True, db_index=True)
    ynr_person_name = models.CharField(blank=True, null=True, max_length=255)
    ballot_id = models.CharField(
        blank=True, null=True, max_length=255, db_index=True
    )
    election = models.ForeignKey(Election, null=True, on_delete=models.CASCADE)
    constituency = models.ForeignKey(
        Constituency, blank=True, null=True, on_delete=models.CASCADE
    )
    imprint = models.TextField(blank=True, null=True)
    postcode = models.CharField(max_length=150, blank=True)
    name = models.CharField(blank=True, max_length=300)
    email = models.CharField(blank=True, max_length=300)
    date_uploaded = models.DateTimeField(auto_now_add=True)
    date_delivered = models.DateTimeField(blank=True, null=True)
    status = models.CharField(
        choices=constants.LEAFLET_STATUSES,
        null=True,
        blank=True,
        max_length=255,
    )
    reviewed = models.BooleanField(default=False)

    objects = models.Manager()

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ("-date_uploaded",)

    def get_absolute_url(self):
        from django.contrib.sites.models import Site

        return "http://%s/leaflets/%s/" % (
            Site.objects.get_current().domain,
            self.id,
        )

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
            return "%s leaflet" % self.publisher_party.party_name
        else:
            "Untitled leaflet"

    def get_person(self):
        if (
            self.ynr_person_id
            and self.ynr_person_name
            and not self.publisher_person
        ):
            return {
                "link": reverse(
                    "person", kwargs={"remote_id": self.ynr_person_id}
                ),
                "name": self.ynr_person_name,
            }
        elif self.publisher_person:
            return {
                "link": reverse(
                    "person",
                    kwargs={"remote_id": self.publisher_person.remote_id},
                ),
                "name": self.publisher_person.name,
            }

    def get_party(self):
        if self.ynr_party_id and self.ynr_party_name:
            pp_id = "PP{}".format(re.sub(r"party:", "", self.ynr_party_id))
            return {
                "link": reverse("party-view", kwargs={"pk": pp_id}),
                "name": self.ynr_party_name,
            }
        elif self.publisher_party:
            return {
                "link": reverse(
                    "party-view", kwargs={"pk": self.publisher_party.pk}
                ),
                "name": self.publisher_party.party_name,
            }

    def get_ballot(self):
        if self.ballot_id:
            r = devs_dc_helper.ballot_request(self.ballot_id)
            if r.status_code == 200:
                ballot = r.json()
                return {
                    "name": "{} in {}".format(
                        ballot["election_title"],
                        ballot["election_type"]["name"],
                    ),
                    "link": "https://whocanivotefor.co.uk/elections/{}".format(
                        self.ballot_id
                    ),
                }


class LeafletImage(models.Model):
    ORIENTATION_CHOICES = (
        (1, "Horizontal (normal)"),
        (2, "Mirror horizontal"),
        (3, "Rotate 180"),
        (4, "Mirror vertical"),
        (5, "Mirror horizontal and rotate 270 CW"),
        (6, "Rotate 90 CW"),
        (7, "Mirror horizontal and rotate 90 CW"),
        (8, "Rotate 270 CW"),
    )

    leaflet = models.ForeignKey(
        Leaflet, related_name="images", on_delete=models.CASCADE
    )
    image = ImageField(upload_to="leaflets", max_length=255)
    raw_image = ImageField(upload_to="raw_leaflets", blank=True, max_length=255)
    legacy_image_key = models.CharField(max_length=255, blank=True)
    image_type = models.CharField(
        choices=constants.IMAGE_TYPES, null=True, blank=True, max_length=255
    )
    orientation = models.PositiveSmallIntegerField(
        choices=ORIENTATION_CHOICES, default=1
    )
    exif_data = models.BinaryField(null=True, blank=True)

    class Meta:
        ordering = ["image_type"]

    def _remove_exif_data(self):
        full_image = Image.open(self.image)

        if full_image.info.get("exif"):
            exif_dict = piexif.load(full_image.info["exif"])
            orientation = exif_dict.get("0th", {}).get(
                piexif.ImageIFD.Orientation, 1
            )

            self.orientation = orientation
            self.exif_data = full_image.info["exif"]
        else:
            self.exif_data = b""

        data = list(full_image.getdata())
        image_without_exif = Image.new(full_image.mode, full_image.size)
        image_without_exif.putdata(data)

        rotated_image = self._correctly_orient_image(image_without_exif)

        new_file = BytesIO()
        rotated_image = rotated_image.convert("RGB")
        rotated_image.save(new_file, "jpeg")
        file_content = ContentFile(new_file.getvalue())

        self.image.save(self.image.name, file_content, save=False)

    def _correctly_orient_image(self, image):
        if self.orientation == 3:
            return image.transpose(Image.ROTATE_180)
        elif self.orientation == 6:
            return image.transpose(Image.ROTATE_270)
        elif self.orientation == 8:
            return image.transpose(Image.ROTATE_90)
        return image

    def save(self, *args, **kwargs):
        """
        Save a copy of the raw_image as soon as possible.

        This is so we don't destroy images, by cropping them too small
        for example.
        """
        # if not self.exif_data and self.exif_data != b"":
        #     self._remove_exif_data()

        super(LeafletImage, self).save(*args, **kwargs)
        if not self.raw_image:
            self.raw_image.save(self.image.name, self.image.file)
        # self._clean_image()

    def _clean_image(self):
        from sorl.thumbnail.engines.pil_engine import Engine
        from sorl.thumbnail.images import ImageFile

        e = Engine()
        f = ImageFile(self.image.file)
        tmp_image = e.get_image(f)

        new_file = BytesIO()
        tmp_image = tmp_image.convert("RGB")
        tmp_image.save(new_file, "jpeg")
        file_content = ContentFile(new_file.getvalue())

        self.image.save(self.image.name, file_content, save=False)

    def get_absolute_url(self):
        return reverse("full_image", kwargs={"pk": self.pk})

    @property
    def dimensions(self):
        im = Image.open(self.image.path)
        return im.size

    def crop(self, x=None, y=None, x2=None, y2=None):
        if not all((x, y, x2, y2)):
            raise ValueError("All points are required")
        file_name = self.raw_image.name
        im = Image.open(self.raw_image.file)
        cropped = im.copy()
        cropped = cropped.crop((x, y, x2, y2))
        new_file = BytesIO()
        cropped = cropped.convert("RGB")
        cropped.save(new_file, "jpeg")
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
            new_file = BytesIO()
            rotated = rotated.convert("RGB")
            rotated.save(new_file, "jpeg")
            file_content = ContentFile(new_file.getvalue())
            image_field.save(file_name, file_content)
            delete(self.image, delete_file=False)
