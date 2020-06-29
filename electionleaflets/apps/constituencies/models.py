from django.db import models
from django.urls import reverse
from django_extensions.db.fields import AutoSlugField


class Constituency(models.Model):
    constituency_id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=765)
    country_name = models.CharField(max_length=255)

    alternative_name = models.CharField(max_length=765, blank=True)
    retired = models.IntegerField(null=True, blank=True)
    slug = AutoSlugField(populate_from="name", max_length=255, separator="_")
    count = models.IntegerField(null=True)

    # Not used anywhere
    wikipedia_url = models.CharField(max_length=765, blank=True)
    url_id = models.CharField(max_length=300, blank=True)
    guardian_aristotle_id = models.IntegerField(null=True, blank=True)
    guardian_pa_code = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Constituencies"

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            "constituency-view", (), {"pk": self.pk, "ignored_slug": self.slug,}
        )
