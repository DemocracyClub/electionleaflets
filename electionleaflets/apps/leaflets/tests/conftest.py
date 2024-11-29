from pathlib import Path
from unittest.mock import patch

import boto3
import pytest
from django.core.files.storage import default_storage
from moto import mock_aws

TEST_IMAGE_LOCATION = Path(__file__).parent / "test_images/front_test.jpg"


@pytest.fixture()
def uploaded_temp_file():
    """
    The application uploads images to a temp location before
    moving them to the final location and saving the LeafletImage model.

    This fixture gives us a file in a temp media location, as if it had just
    been uploaded.

    :return:
    """

    path = "test-leaflet.jpeg"
    with default_storage.open(path, "wb") as f:
        f.write(TEST_IMAGE_LOCATION.read_bytes())
    return path


@pytest.fixture
def mock_get_ballot_data_from_ynr():
    def _mock_ynr_value(return_value):
        return patch(
            "leaflets.forms.PartyForm.get_ballot_data_from_ynr",
            return_value=return_value,
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
    return s3_client.create_bucket(Bucket=settings.AWS_STORAGE_BUCKET_NAME)
