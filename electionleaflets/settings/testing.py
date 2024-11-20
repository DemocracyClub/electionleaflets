import os
from .base import *  # noqa: F403
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
STATICFILES_STORAGE = "electionleaflets.storages.StaticStorage"

MEDIA_ROOT = root("test_media",)  # noqa: F405

INSTALLED_APPS.append("aloe_django")  # noqa: F405
YNR_API_KEY = "testing"
WHITENOISE_USE_FINDERS = True
WHITENOISE_AUTOREFRESH = True
DEBUG = False
