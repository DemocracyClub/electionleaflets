import os

from .base import *  # noqa: F403

DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
STATICFILES_STORAGE = "django.core.files.storage.FileSystemStorage"
TEST_RUNNER = "django.test.runner.DiscoverRunner"

MEDIA_ROOT = MEDIA_ROOT = root("test_media",)  # noqa: F405

INSTALLED_APPS.append("aloe_django")  # noqa: F405
