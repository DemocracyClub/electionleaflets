import factory
import pytest
from core.models import Country, EmailAlert, EmailQue, ImageQue, ImageQueSeq
from factory.django import DjangoModelFactory


class CountryFactory(DjangoModelFactory):
    class Meta:
        model = Country

    country_id = factory.Sequence(lambda n: n)
    iso = factory.Sequence(lambda n: "ISO%d" % n)
    name = factory.Sequence(lambda n: "Country %d" % n)
    iso3 = factory.Sequence(lambda n: "ISO3%d" % n)


class EmailAlertFactory(DjangoModelFactory):
    class Meta:
        model = EmailAlert

    email_alert_id = factory.Sequence(lambda n: n)
    email = factory.Sequence(lambda n: "user%d@example.com" % n)
    frequency_hours = 24
    last_sent = None
    type = factory.Sequence(lambda n: "Type %d" % n)
    parent_id = factory.Sequence(lambda n: n)
    activated = 1
    confirm_id = factory.Sequence(lambda n: "Confirm%d" % n)
    title = factory.Sequence(lambda n: "Title %d" % n)


class EmailQueFactory(DjangoModelFactory):
    class Meta:
        model = EmailQue

    email_que_id = factory.Sequence(lambda n: n)
    name = factory.Sequence(lambda n: "Name %d" % n)
    email = factory.Sequence(lambda n: "user%d@example.com" % n)
    postcode = factory.Sequence(lambda n: "Postcode %d" % n)
    delivery_date = factory.Faker("date_time")


class ImageQueFactory(DjangoModelFactory):
    class Meta:
        model = ImageQue

    image_que_id = factory.Sequence(lambda n: n)
    upload_key = factory.Sequence(lambda n: "UploadKey%d" % n)
    name = factory.Sequence(lambda n: "Name %d" % n)
    email = factory.Sequence(lambda n: "user%d@example.com" % n)
    image_key = factory.Sequence(lambda n: "ImageKey%d" % n)
    uploaded_date = factory.Faker("date_time")


class ImageQueSeqFactory(DjangoModelFactory):
    class Meta:
        model = ImageQueSeq

    sequence = factory.Sequence(lambda n: n)


@pytest.mark.django_db
def test_country_creation():
    country = CountryFactory()
    assert country.name.startswith("Country")


@pytest.mark.django_db
def test_email_alert_creation():
    email_alert = EmailAlertFactory()
    assert email_alert.email.startswith("user")
    assert email_alert.frequency_hours == 24


@pytest.mark.django_db
def test_email_que_creation():
    email_que = EmailQueFactory()
    assert email_que.email.startswith("user")
    assert email_que.postcode.startswith("Postcode")


@pytest.mark.django_db
def test_image_que_creation():
    image_que = ImageQueFactory()
    assert image_que.upload_key.startswith("UploadKey")
    assert image_que.image_key.startswith("ImageKey")


@pytest.mark.django_db
def test_image_que_seq_creation():
    image_que_seq = ImageQueSeqFactory()
    assert isinstance(image_que_seq.sequence, int)
