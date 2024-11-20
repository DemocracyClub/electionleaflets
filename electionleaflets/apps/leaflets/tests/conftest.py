from unittest.mock import patch

import boto3
import pytest
from django.core.files.storage import default_storage

from moto import mock_aws

@pytest.fixture
def mock_get_ballot_data_from_ynr():
    def _mock_ynr_value(return_value):
        return patch(
            "leaflets.forms.PartyForm.get_ballot_data_from_ynr",
            return_value=return_value
        )
    return _mock_ynr_value



@pytest.fixture
def s3_client():
    """Fixture to provide a mocked S3 client."""
    # Initialize the mocked S3 client
    with mock_aws():
        client = boto3.client("s3")
        yield client

@pytest.fixture
def s3_bucket(s3_client, settings):
    bucket = s3_client.create_bucket(Bucket=settings.AWS_STORAGE_BUCKET_NAME)
    return bucket
