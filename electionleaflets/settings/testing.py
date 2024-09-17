from .base import INSTALLED_APPS, root  # noqa: F403

MEDIA_ROOT = MEDIA_ROOT = root("test_media",)  # noqa: F405


INSTALLED_APPS.append("aloe_django")  # noqa: F405
