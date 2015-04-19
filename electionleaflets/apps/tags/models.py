from django.db import models
from django_extensions.db.fields import AutoSlugField

class Tag(models.Model):
    tag = models.CharField(max_length=765)
    tag_clean = models.CharField(max_length=765, blank=True)
    slug = AutoSlugField(populate_from='tag', max_length=255, separator=u'_')
    dead = models.IntegerField(null=True, blank=True)
    
    def __unicode__(self):
        return self.tag
    
    class Meta:
        db_table = u'tag'
        