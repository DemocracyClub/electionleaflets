from django.db import models
from django_extensions.db.models import TimeStampedModel

from django.contrib.auth.models import User

from leaflets.models import Leaflet


class LeafletProperties(TimeStampedModel):
    leaflet = models.ForeignKey(Leaflet)
    user = models.ForeignKey(User)
    key = models.CharField(blank=True, max_length=100, db_index=True)
    value = models.CharField(blank=True, max_length=255, db_index=True)
