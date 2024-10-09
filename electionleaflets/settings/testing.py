import os

from .base import *  # noqa: F403

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
STATICFILES_STORAGE = "electionleaflets.storages.StaticStorage"
TEST_RUNNER = "django.test.runner.DiscoverRunner"

MEDIA_ROOT = root("test_media",)  # noqa: F405

INSTALLED_APPS.append("aloe_django")  # noqa: F405
YNR_API_KEY = "testing"
