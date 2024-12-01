import os
from tempfile import mkdtemp

from .base import *  # noqa: F403

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

DEFAULT_FILE_STORAGE = "electionleaflets.storages.TempUploadLocalMediaStorage"
STATICFILES_STORAGE = "electionleaflets.storages.StaticStorage"

# This is cleaned up in core/conftest.py
MEDIA_ROOT = mkdtemp()

YNR_API_KEY = "testing"
WHITENOISE_USE_FINDERS = True
WHITENOISE_AUTOREFRESH = True
DEBUG = False
