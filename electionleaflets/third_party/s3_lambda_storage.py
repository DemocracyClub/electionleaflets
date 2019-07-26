from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class S3StaticStorage(S3Boto3Storage):
    def __init__(self, *args, **kwargs):
        kwargs['location'] = settings.STATIC_URL
        super(S3StaticStorage, self).__init__(*args, **kwargs)
