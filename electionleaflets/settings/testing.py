from .base import *

LETTUCE_USE_TEST_DATABASE = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/tmp/electionleaflets.db',
    }
}