from django.db import models


class Country(models.Model):
    country_id = models.IntegerField(primary_key=True)
    iso = models.CharField(max_length=6)
    name = models.CharField(max_length=240)
    iso3 = models.CharField(max_length=9, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = "country"
        verbose_name_plural = "Countries"


class EmailAlert(models.Model):
    email_alert_id = models.IntegerField(primary_key=True)
    email = models.CharField(max_length=150)
    frequency_hours = models.IntegerField()
    last_sent = models.DateTimeField(null=True, blank=True)
    type = models.CharField(max_length=150)
    parent_id = models.IntegerField()
    activated = models.IntegerField(null=True, blank=True)
    confirm_id = models.CharField(max_length=300)
    title = models.CharField(max_length=765)

    class Meta:
        db_table = "email_alert"
        verbose_name_plural = "Email alerts"


class EmailQue(models.Model):
    email_que_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=765, blank=True)
    email = models.CharField(max_length=765)
    postcode = models.CharField(max_length=60)
    delivery_date = models.DateTimeField()

    class Meta:
        db_table = "email_que"


class ImageQue(models.Model):
    image_que_id = models.IntegerField(primary_key=True)
    upload_key = models.CharField(max_length=765)
    name = models.CharField(max_length=300, blank=True)
    email = models.CharField(max_length=300, blank=True)
    image_key = models.CharField(max_length=765, blank=True)
    uploaded_date = models.DateTimeField()

    class Meta:
        db_table = "image_que"


class ImageQueSeq(models.Model):
    sequence = models.IntegerField(primary_key=True)

    class Meta:
        db_table = "image_que_seq"
