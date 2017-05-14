import boto3
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
