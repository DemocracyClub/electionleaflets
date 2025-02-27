from pathlib import Path

import boto3
import pytest
from moto import mock_aws

# Constants used for testing
TEST_BUCKET = "leaflet-test-thumbs"
TEST_IMAGES_PATH = Path(__file__).parent / "test_images"


@pytest.fixture
def mock_s3_bucket(monkeypatch):
    monkeypatch.setenv("LEAFLET_IMAGES_BUCKET_NAME", TEST_BUCKET)

    with mock_aws():
        s3 = boto3.client("s3")
        s3.create_bucket(Bucket=TEST_BUCKET)
        yield s3
        # Clean up after
        objects = s3.get_paginator("list_objects_v2")
        objects_iterator = objects.paginate(Bucket=TEST_BUCKET)
        for page in objects_iterator:
            if "Contents" in page:
                objects = [{"Key": obj["Key"]} for obj in page["Contents"]]
                s3.delete_objects(
                    Bucket=TEST_BUCKET, Delete={"Objects": objects}
                )
        s3.delete_bucket(Bucket=TEST_BUCKET)


IMAGES_TO_TEST = (
    TEST_IMAGES_PATH / "front_test.jpg",
    TEST_IMAGES_PATH / "heif_test.heif",
    TEST_IMAGES_PATH / "tiff_test.tiff",
)


@pytest.mark.parametrize("image_filename", IMAGES_TO_TEST)
def test_handle_s3_creates_thumbnails(
    image_filename,
    mock_s3_bucket,
):
    mock_s3_bucket.put_object(
        Bucket=TEST_BUCKET,
        Key=f"leaflets/{image_filename.name}",
        Body=image_filename.read_bytes(),
    )

    event = {
        "Records": [
            {
                "s3": {
                    "bucket": {"name": TEST_BUCKET},
                    "object": {"key": f"leaflets/{image_filename.name}"},
                }
            }
        ]
    }
    from thumbs.handler import handle_s3

    handle_s3(event, context=None, local=False)

    all_objects = mock_s3_bucket.list_objects_v2(Bucket=TEST_BUCKET)
    keys = [obj["Key"] for obj in all_objects.get("Contents", [])]
    print(keys)
    expected_starts = [
        f"thumbs/350/crop=top/leaflets/{image_filename.name}",
        f"thumbs/150/crop=noop/leaflets/{image_filename.name}",
        f"thumbs/1000/crop=noop/leaflets/{image_filename.name}",
        f"thumbs/600/crop=center/leaflets/{image_filename.name}",
        f"thumbs/350/leaflets/{image_filename.name}",
        f"thumbs/600/leaflets/{image_filename.name}",
    ]

    for expected_key in expected_starts:
        assert expected_key in keys, f"{expected_key} not found in S3 objects."


@pytest.mark.parametrize("image_filename", IMAGES_TO_TEST)
def test_handle_cf_creates_thumbnails(
    image_filename,
    mock_s3_bucket,
):
    mock_s3_bucket.put_object(
        Bucket=TEST_BUCKET,
        Key=f"leaflets/{image_filename.name}",
        Body=image_filename.read_bytes(),
    )
    from thumbs.handler import handle

    paths = (
        f"thumbs/350/leaflets/{image_filename.name}",
        f"thumbs/350/crop=top/leaflets/{image_filename.name}",
    )

    for path in paths:
        event = {
            "Records": [
                {
                    "cf": {
                        "request": {
                            # CF expects a starting slash
                            "uri": f"/{path}"
                        },
                        "response": {"status": "404", "headers": {}},
                    }
                }
            ]
        }
        handle(event, context=None)

    all_objects = mock_s3_bucket.list_objects_v2(Bucket=TEST_BUCKET)
    keys = [obj["Key"] for obj in all_objects.get("Contents", [])]

    for expected_key in paths:
        assert expected_key in keys, f"{expected_key} not found in S3 objects."
