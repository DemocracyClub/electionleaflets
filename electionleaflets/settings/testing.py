import os

from .base import *

LETTUCE_USE_TEST_DATABASE = True
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

MEDIA_ROOT = MEDIA_ROOT = root('test_media', )

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.spatialite',
        'NAME': '/tmp/electionleaflets.db',
    },
    # 'test': {
    #     'ENGINE': 'django.contrib.gis.db.backends.spatialite',
    #     'NAME': '/tmp/electionleaflets.db',
    # }
}

if os.environ.get('RUNNER') == "travis":
    DATABASES = {
        'default': {
            'ENGINE': 'django.contrib.gis.db.backends.postgis',
            'NAME': 'travis_ci_test',
            'USER': 'postgres',
        }
    }
