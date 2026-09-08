from urllib.parse import urlparse

import pytest
from django.conf import settings
from django.urls import reverse
from leaflets.models import LeafletImage

from .helpers import create_dummy_leaflets


@pytest.fixture
def leaflet_image():
    create_dummy_leaflets()
    return LeafletImage.objects.last()


@pytest.fixture
def staff_user(django_user_model):
    return django_user_model.objects.create_user(
        username="staff", password="password", is_staff=True
    )


@pytest.fixture
def normal_user(django_user_model):
    return django_user_model.objects.create_user(
        username="normal", password="password"
    )


@pytest.mark.django_db
class TestImageViewAccess:
    """`full_image`: anonymous GET is allowed, POST requires a staff user."""

    def test_get_anonymous_allowed(self, client, leaflet_image):
        url = reverse("full_image", kwargs={"pk": leaflet_image.pk})
        response = client.get(url)
        assert response.status_code == 200

    def test_post_anonymous_redirects_to_login(self, client, leaflet_image):
        url = reverse("full_image", kwargs={"pk": leaflet_image.pk})
        response = client.post(url, {})
        assert response.status_code == 302
        assert urlparse(response.url).path == settings.LOGIN_URL

    def test_post_non_staff_forbidden(self, client, normal_user, leaflet_image):
        client.force_login(normal_user)
        url = reverse("full_image", kwargs={"pk": leaflet_image.pk})
        response = client.post(url, {})
        assert response.status_code == 403

    def test_post_staff_allowed(self, client, staff_user, leaflet_image):
        client.force_login(staff_user)
        url = reverse("full_image", kwargs={"pk": leaflet_image.pk})
        response = client.post(url, {})
        # permission check passes and the form is processed (not 302-to-login/403)
        assert response.status_code == 302
        assert response.url == url


@pytest.mark.django_db
class TestImageCropViewAccess:
    """`crop` requires a staff user for both GET and POST."""

    def test_get_anonymous_redirects_to_login(self, client, leaflet_image):
        url = reverse("crop", kwargs={"pk": leaflet_image.pk})
        response = client.get(url)
        assert response.status_code == 302
        assert urlparse(response.url).path == settings.LOGIN_URL

    def test_get_non_staff_forbidden(self, client, normal_user, leaflet_image):
        client.force_login(normal_user)
        url = reverse("crop", kwargs={"pk": leaflet_image.pk})
        response = client.get(url)
        assert response.status_code == 403

    def test_get_staff_allowed(self, client, staff_user, leaflet_image):
        client.force_login(staff_user)
        url = reverse("crop", kwargs={"pk": leaflet_image.pk})
        response = client.get(url)
        assert response.status_code == 200


@pytest.mark.django_db
class TestImageRotateViewAccess:
    """`rotate` requires a staff user for both GET and POST."""

    def test_get_anonymous_redirects_to_login(self, client, leaflet_image):
        url = reverse("rotate", kwargs={"pk": leaflet_image.pk})
        response = client.get(url)
        assert response.status_code == 302
        assert urlparse(response.url).path == settings.LOGIN_URL

    def test_get_non_staff_forbidden(self, client, normal_user, leaflet_image):
        client.force_login(normal_user)
        url = reverse("rotate", kwargs={"pk": leaflet_image.pk})
        response = client.get(url)
        assert response.status_code == 403

    def test_get_staff_allowed(self, client, staff_user, leaflet_image):
        client.force_login(staff_user)
        url = reverse("rotate", kwargs={"pk": leaflet_image.pk})
        response = client.get(url)
        assert response.status_code == 200


@pytest.mark.django_db
class TestLeafletModerationAccess:
    """`moderate` requires any logged-in user."""

    def test_get_anonymous_redirects_to_login(self, client):
        response = client.get(reverse("moderate"))
        assert response.status_code == 302
        assert urlparse(response.url).path == settings.LOGIN_URL

    def test_get_logged_in_allowed(self, client, normal_user):
        client.force_login(normal_user)
        response = client.get(reverse("moderate"))
        assert response.status_code == 200
