import os

from .base import *  # noqa: F403

DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

MEDIA_ROOT = MEDIA_ROOT = root('test_media', )  # noqa: F405

if os.environ.get('RUNNER') == "travis":
    DATABASES = {
        'default': {
            'ENGINE': 'django.contrib.gis.db.backends.postgis',
            'NAME': 'travis_ci_test',
            'USER': 'postgres',
        }
    }

INSTALLED_APPS.append('aloe_django')  # noqa: F405
