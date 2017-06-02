import boto3
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class S3LambdaStorage(S3Boto3Storage):
    @property
    def connection(self):
        if self._connection is None:
            session = boto3.session.Session()
            self._connection = session.resource(
                self.connection_service_name,
                region_name=self.region_name,
                use_ssl=self.use_ssl,
                endpoint_url=self.endpoint_url,
                config=self.config
            )
        return self._connection


class S3StaticLambdaStorage(S3LambdaStorage):
    def __init__(self, *args, **kwargs):
        kwargs['location'] = settings.STATIC_URL
        super(S3StaticLambdaStorage, self).__init__(*args, **kwargs)
