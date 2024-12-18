import os.path
import re
from io import BytesIO
from pathlib import Path

import piexif
from core.helpers import YNRAPIHelper
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db import models
from django.db.models import JSONField
from django.forms.models import model_to_dict
from django.urls import reverse
from PIL import Image
from slugify import slugify
from sorl.thumbnail import ImageField, delete

from electionleaflets.storages import TempUploadBaseMixin

from . import constants


class Leaflet(models.Model):
    def __init__(self, *args, **kwargs):
        super(Leaflet, self).__init__(*args, **kwargs)
        self._initial = model_to_dict(
            self, fields=[field.name for field in self._meta.fields]
        )

    title = models.CharField(blank=True, max_length=765)
    description = models.TextField(blank=True, null=True)
    ynr_party_id = models.CharField(
        blank=True, null=True, max_length=255, db_index=True
    )
    ynr_party_name = models.CharField(blank=True, null=True, max_length=255)
    ynr_person_id = models.IntegerField(blank=True, null=True, db_index=True)
    ynr_person_name = models.CharField(blank=True, null=True, max_length=255)
    ballot_id = models.CharField(
        blank=True, null=True, max_length=255, db_index=True
    )

    ballots = JSONField(default=list)
    people = JSONField(default=dict)
    person_ids = JSONField(default=list)

    imprint = models.TextField(blank=True, null=True)
    postcode = models.CharField(max_length=150, blank=True)
    nuts1 = models.CharField(max_length=3, blank=True)
    name = models.CharField(blank=True, max_length=300)
    email = models.CharField(blank=True, max_length=300)
    date_uploaded = models.DateTimeField(auto_now_add=True)
    date_delivered = models.DateTimeField(blank=True, null=True)
    status = models.CharField(
        choices=constants.LEAFLET_STATUSES,
        null=True,
        blank=True,
        max_length=255,
        default="draft",
    )
    modified = models.DateTimeField(auto_now=True)
    reviewed = models.BooleanField(default=False)

    objects = models.Manager()

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ("-date_uploaded",)

    def get_full_url(self):
        from django.contrib.sites.models import Site

        return "http://%s/leaflets/%s/" % (
            Site.objects.get_current().domain,
            self.get_absolute_url(),
        )

    def get_absolute_url(self):
        return reverse("leaflet", kwargs={"pk": self.pk})

    def get_first_image(self):
        try:
            return self.images.all()[0]
        except IndexError:
            # TODO: Set image_key to value for 'empty' image
            return None

    def get_title(self):
        if self.title and len(self.title):
            return self.title
        if self.ynr_party_name:
            return f"{self.ynr_party_name} leaflet"
        return None

    def get_person(self):
        if self.ynr_person_id and self.ynr_person_name:
            return {
                "link": reverse(
                    "person", kwargs={"remote_id": self.ynr_person_id}
                ),
                "name": self.ynr_person_name,
            }
        return None

    def get_party(self):
        if self.ynr_party_id and self.ynr_party_name:
            pp_id = "PP{}".format(re.sub(r"party:", "", self.ynr_party_id))
            return {
                "link": reverse("party-view", kwargs={"pk": pp_id}),
                "name": self.ynr_party_name,
            }

        return None

    def attach_nuts_code(self) -> None:
        """
        Gets a NUTS1 code from YNR.

        This is a little hacky: we might not have a ballot for a postcode at the
        point we look up that postcode. But we want a NUTS1 code for every
        uploaded leaflet.

        Because of this, we pick a known UK-wide election date and look up
        what the NUTS1 code of that ballot ID was. This in imperfect for
        most geographies, but NUTS1 are big enough that we don't care about
        (literal) edge cases.

        """

        params = {
            "for_postcode": self.postcode,
            "election_type": "parl",
            "election_date": "2024-07-04",
        }
        ynr_helper = YNRAPIHelper()

        resp = ynr_helper.get("ballots", params=params)
        self.nuts1 = resp["results"][0]["tags"].get("NUTS1", {}).get("key")
        self.save()


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
    image = ImageField(max_length=255)
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
        ordering = ["pk", "image_type"]

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
        if self.orientation == 6:
            return image.transpose(Image.ROTATE_270)
        if self.orientation == 8:
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

    def set_image_from_temp_file(self, temp_file):
        """
        As part of the leaflet upload process we save images to
        a temporary location when accepting files in the wizard.

        When we make a Leaflet and LeafletImages we need to move the
        files from the temp location to the live location.

        In production this is done using two S3 buckets. We do this
        so that we can set up triggers on the 'live' bucket for making
        thumbnails etc, and have a scratch bucket for random uploads.

        In dev we do the same sort of thing except both files are local.

        The logic for this is defined in the storage backends.

        For this to work, we need a storage backend that uses an implementation
        of `TempUploadBaseMixin`.

        This is a helper function for driving those backends.

        """

        if not self.leaflet_id:
            raise ValueError(
                "Parent Leaflet instance needs to be saved "
                "before a LeafletImage can be created"
            )

        if not isinstance(default_storage, TempUploadBaseMixin):
            raise ValueError("Storage class needs to use `TempUploadBaseMixin`")
        file_name, ext = os.path.basename(temp_file).rsplit(".")
        target_file_path = Path(
            f"leaflets/{self.leaflet.pk}/{slugify(file_name)}.{ext}"
        )

        default_storage.save_from_temp_upload(temp_file, target_file_path)
        self.image.name = str(target_file_path)
