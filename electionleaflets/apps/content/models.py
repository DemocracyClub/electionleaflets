from django.db import models


class ContentBlock(models.Model):
    """
    A simple block of HTML content that can be used by various sections of the 
    site based on the provided name, which acts as a key.
    """
    name = models.CharField(max_length=64)
    content = models.TextField(blank=True)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        db_table = u'contentblock'
