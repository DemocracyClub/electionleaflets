from .base import *

LETTUCE_USE_TEST_DATABASE = True
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

MEDIA_ROOT = MEDIA_ROOT = root('test_media', )

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/tmp/electionleaflets.db',
    }
}