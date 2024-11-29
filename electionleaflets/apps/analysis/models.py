from django.contrib.auth.models import User
from django.db import models
from django_extensions.db.models import TimeStampedModel
from leaflets.models import Leaflet


class LeafletPropertiesQuerySet(models.QuerySet):
    def leaders_photo_count(self):
        return self.filter(key="has_leader_photo", value="Yes").count()

    def opposition_photo_count(self):
        return self.filter(key="has_opposition_leader", value="Yes").count()

    def leaders_mentions(self):
        return self.filter(key="has_leader", value="Yes").count()

    def squeeze_messages_count(self):
        return self.filter(key="squeeze_message", value="Yes").count()

    def opposition_mentions_count(self):
        return self.filter(
            key="has_opposition_leader_photo", value="Yes"
        ).count()

    def leaflet_type_count(self, leaflet_type):
        return self.filter(key="leaflet_style", value=leaflet_type).count()

    def party_logo(self):
        return self.filter(key="has_logo", value="Yes").count()

    def graphs_count(self):
        return self.filter(key="include_graph", value="Yes").count()

    def leaflets_analysed(self):
        return self.order_by().values_list("leaflet").distinct().count()


class LeafletPropertiesManager(models.Manager):
    def get_queryset(self):
        return LeafletPropertiesQuerySet(self.model, using=self._db)


class LeafletProperties(TimeStampedModel):
    leaflet = models.ForeignKey(Leaflet, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.CharField(blank=True, max_length=100, db_index=True)
    value = models.CharField(blank=True, max_length=255, db_index=True)

    objects = LeafletPropertiesManager()
