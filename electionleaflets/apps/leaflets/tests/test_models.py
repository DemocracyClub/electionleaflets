from pathlib import Path

import pytest
from leaflets.models import Leaflet, LeafletImage
from leaflets.tests.conftest import TEST_IMAGE_LOCATION


@pytest.fixture
def leaflet():
    return Leaflet.objects.create(title="Test Leaflet", description=None)



@pytest.mark.django_db
def test_model_initial():
    leaflet = Leaflet()
    assert leaflet._initial == {
        "id": None,
        "title": "",
        "description": None,
        "ynr_party_id": None,
        "ynr_party_name": None,
        "ynr_person_id": None,
        "ynr_person_name": None,
        "ballot_id": None,
        "ballots": [],
        "people": {},
        "person_ids": [],
        "election": None,
        "imprint": None,
        "postcode": "",
        "name": "",
        "email": "",
        "date_delivered": None,
        "status": "draft",
        "reviewed": False,
    }
    assert leaflet._initial["status"] == "draft"


@pytest.mark.django_db
def test_markdown_error(client, leaflet):
    response = client.get(leaflet.get_absolute_url())
    assert response.status_code == 200


@pytest.mark.django_db
def test_leaflet_detail(client):
    leaflet = Leaflet.objects.create(
        title="Test Leaflet",
        description=None,
        ynr_party_id="party:1",
        ynr_party_name="Labour Party",
    )
    response = client.get(leaflet.get_absolute_url())
    assert response.status_code == 200
    assert "Test Leaflet" in response.content.decode()
    assert "Labour Party" in response.content.decode()


@pytest.mark.django_db
def test_raw_image_field():
    leaflet = Leaflet()
    leaflet.save()
    li = LeafletImage(leaflet=leaflet)
    assert li.raw_image.name == ""
    with TEST_IMAGE_LOCATION.open("rb") as img_file:
        li.image.save("front_test.jpg", img_file)
    assert "front_test" in li.raw_image.name


def test_save_leaflet_image_from_temp_file(db):
    leaflet_image = LeafletImage()
    with pytest.raises(ValueError) as e_info:
        leaflet_image.set_image_from_temp_file("/not/a/path")
    assert str(e_info.value) == (
        "Parent Leaflet instance needs to be saved "
        "before a LeafletImage can be created"
    )


def test_image_moved_from_temp_upload(db, uploaded_temp_file):
    leaflet = Leaflet()
    leaflet.save()
    leaflet.refresh_from_db()
    leaflet_image = LeafletImage(leaflet=leaflet)
    leaflet_image.set_image_from_temp_file(uploaded_temp_file)
    leaflet_image.save()
    leaflet_image.refresh_from_db()

    path = (
        Path(leaflet_image.image.storage.base_location)
        / f"leaflets/{leaflet.pk}/test-leaflet.jpeg"
    )
    assert str(path) == leaflet_image.image.path


def test_image_moved_from_temp_upload_s3_backend(
    db, settings, s3_bucket, s3_client
):
    settings.DEFAULT_FILE_STORAGE = (
        "electionleaflets.storages.TempUploadS3MediaStorage"
    )
    leaflet = Leaflet()
    leaflet.save()
    leaflet.refresh_from_db()
    leaflet_image = LeafletImage(leaflet=leaflet)
    s3_client.put_object(
        Key="test_images/test_leaflet.jpeg",
        Body="",
        Bucket=settings.AWS_STORAGE_BUCKET_NAME,
    )
    leaflet_image.set_image_from_temp_file("test_images/test_leaflet.jpeg")
    leaflet_image.save()
    leaflet_image.refresh_from_db()

    key = f"leaflets/{leaflet.pk}/test-leaflet.jpeg"

    assert s3_client.head_object(
        Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=key
    )
    assert str(key) == leaflet_image.image.file.name
