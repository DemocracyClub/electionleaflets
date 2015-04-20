from django.db import models


class Election(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    country = models.ForeignKey('core.Country', null=True, blank=True)

    live_date = models.DateTimeField()
    dead_date = models.DateTimeField()
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

