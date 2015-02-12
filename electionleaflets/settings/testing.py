from .base import *

LETTUCE_USE_TEST_DATABASE = True
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/tmp/electionleaflets.db',
    }
}