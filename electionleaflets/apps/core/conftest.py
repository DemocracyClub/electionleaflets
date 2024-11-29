import os
import shutil
from tempfile import gettempprefix

from django.conf import settings


def pytest_sessionfinish():
    """
    We define `MEDIA_ROOT` as `mktemp()` in our test settings.

    This function simply exists to clean this directory up when testing is done.

    """
    # Don't remove a folder that doesn't exist for some reason
    if not os.path.exists(settings.MEDIA_ROOT):
        return
    # Ensure we've set a temp dir as the MEDIA_ROOT rather than
    # something more important
    assert settings.MEDIA_ROOT.startswith(f"{os.path.sep}{gettempprefix()}")
    # Remove the media root
    shutil.rmtree(settings.MEDIA_ROOT)
