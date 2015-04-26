from django.db import models
from django_extensions.db.models import TimeStampedModel

from leaflets.models import Leaflet

class LeafletProperties(TimeStampedModel):
    leaflet = models.ForeignKey(Leaflet)
    key = models.CharField(blank=True, max_length=100, db_index=True)
    value = models.CharField(blank=True, max_length=255, db_index=True)