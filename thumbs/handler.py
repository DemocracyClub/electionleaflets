import base64
import os
import re
import sys
from io import BytesIO
from os.path import sep
from pathlib import Path

sys.path.append("")
from typing import Tuple
from urllib.parse import unquote

import boto3
import django
import sentry_sdk
from django.conf import settings
from sentry_sdk.integrations.aws_lambda import AwsLambdaIntegration

# Get the bucket name. Because this function is run using Lambda@Edge
# we can't use environment variables there. We want to use these for testing
# so we support getting the value from either.
BUCKET_NAME = None
if leaflet_images_bucket_name := os.environ.get("LEAFLET_IMAGES_BUCKET_NAME"):
    BUCKET_NAME = leaflet_images_bucket_name
else:
    leaflets_bucket_image_path = Path("LEAFLET_IMAGES_BUCKET_NAME")
    if leaflets_bucket_image_path.exists():
        with open("LEAFLET_IMAGES_BUCKET_NAME") as f:
            BUCKET_NAME = f.read().strip()
if not BUCKET_NAME:
    raise ValueError(
        "LEAFLET_IMAGES_BUCKET_NAME needs to exist as an env var or file name"
    )

sentry_dsn_path = Path("SENTRY_DSN")
if sentry_dsn_path.exists():
    with sentry_dsn_path.open() as f:
        SENTRY_DSN = f.read().strip()
        sentry_sdk.init(
            dsn=SENTRY_DSN,
            # Set traces_sample_rate to 1.0 to capture 100%
            # of transactions for tracing.
            traces_sample_rate=0,
            # Set profiles_sample_rate to 1.0 to profile 100%
            # of sampled transactions.
            # We recommend adjusting this value in production.
            profiles_sample_rate=0,
            integrations=[
                AwsLambdaIntegration(),
            ],
        )
if not settings.configured:
    # Pytest will have configured Django, Lambda will not
    # Don't reconfigure settings if already configured,
    # to allow tests to run
    settings.configure()
django.setup()

# These need to be imported after Django has bootstrapped
import pillow_heif  # noqa: E402
from PIL import Image  # noqa: E402
from sorl.thumbnail.base import ThumbnailBackend  # noqa: E402
from sorl.thumbnail.engines import pil_engine  # noqa: E402
from sorl.thumbnail.parsers import parse_geometry  # noqa: E402

client = boto3.client("s3")
engine = pil_engine.Engine()
pillow_heif.register_heif_opener()


def handle(event, context):
    if "s3" in event["Records"][0]:
        return handle_s3(event, context)
    if "cf" in event["Records"][0]:
        return handle_cf(event, context)
    return None


def handle_cf(event, context):
    r = event["Records"][0]

    response = r["cf"]["response"]
    if response["status"] == "200":
        return response

    uri = r["cf"]["request"]["uri"]
    if not uri.startswith("/thumbs"):
        return response

    print("Processing {}".format(uri))

    # ['', 'thumbs', '300', 'crop=center', 'leaflets', 'foo.jpg']
    parts = uri.split(sep)
    parts.pop(0)
    parts.pop(0)
    size = parts.pop(0)

    options = {}
    while "=" in parts[0] or "%3d" in parts[0].lower():
        part = unquote(parts.pop(0))
        k, v = part.split("=")
        options[k] = v

    path = Path(sep.join(parts))

    image = fetch_image(BUCKET_NAME, path)
    processed = process_image(image, (size, options))
    key = new_key((size, options), path)
    upload_image(processed, BUCKET_NAME, key)

    io = BytesIO()
    processed.save(io, "png")

    response["headers"]["content-type"] = [
        {"key": "Content-Type", "value": Image.MIME["PNG"]}
    ]
    response["body"] = re.sub(
        r"\n", "", base64.encodebytes(io.getvalue()).decode("ascii")
    )
    response["bodyEncoding"] = "base64"
    response["status"] = "200"

    return response


def handle_s3(event, context, local=False):
    SPECS = (
        ("350", {"crop": "top"}),
        ("150", {"crop": "noop"}),
        ("1000", {"crop": "noop"}),
        ("600", {"crop": "center"}),
        ("350", {}),
        ("600", {}),
    )

    for r in event["Records"]:
        if not r["s3"]["object"]["key"].startswith("leaflets/"):
            continue
        path = Path(r["s3"]["object"]["key"])
        image = fetch_image(BUCKET_NAME, path)

        for spec in SPECS:
            processed = process_image(image, spec)
            key = new_key(spec, r["s3"]["object"]["key"])
            upload_image(processed, r["s3"]["bucket"]["name"], key)


def fetch_image(bucket: str, key: Path):
    print(key)
    response = client.list_objects_v2(
        Bucket=bucket, Prefix=str(key.with_suffix(""))
    )
    if "Contents" in response:
        object_key = response["Contents"][0]["Key"]
        s3_object = client.get_object(Bucket=bucket, Key=object_key)
        return Image.open(s3_object["Body"])
    raise ValueError(f"Image not found in {response}")


def new_key(spec: tuple, key: Path) -> Path:
    size = spec[0]
    options = spec[1]

    option_parts = [str(size)]
    option_parts.extend(sorted(["=".join(o) for o in list(options.items())]))

    return Path("thumbs/{}/{}".format("/".join(option_parts), key))


def process_image(image: Image, spec: Tuple[str, dict]) -> Image:
    size = spec[0]
    options = spec[1].copy()

    for key, value in list(ThumbnailBackend.default_options.items()):
        options.setdefault(key, value)

    ratio = engine.get_image_ratio(image, options)
    geometry = parse_geometry(size, ratio)
    return engine.create(image, geometry, options)


def upload_image(image: Image, bucket: str, key: Path):
    io = BytesIO()
    image.save(io, "PNG")
    key = key.with_suffix(".png")
    resp = client.put_object(
        ACL="public-read",
        Body=io.getvalue(),
        Bucket=bucket,
        Key=str(key),
        ContentType=Image.MIME["PNG"],
    )
    status_code = resp.get("ResponseMetadata", {}).get("HTTPStatusCode")
    if status_code != 200:
        raise ValueError(
            f"Failed to upload {key} to S3. Status code: {status_code}, Response: {resp}"
        )


if __name__ == "__main__":
    if sys.argv[1] == "--s3":
        handle_s3(
            {
                "Records": [
                    {
                        "s3": {
                            "bucket": {"name": BUCKET_NAME},
                            "object": {"key": "leaflets/image_pX8FVnP.jpg"},
                        }
                    }
                ]
            },
            {},
            True,
        )
    elif sys.argv[1] == "--cf":
        key = "/thumbs/300/crop%3Dtop/leaflets/0439E661-EA19-482F-B11A-454038DE148A.jpeg"
        if sys.argv[2]:
            key = sys.argv[2]

        r = handle_cf(
            {
                "Records": [
                    {
                        "cf": {
                            "request": {"uri": key},
                            "response": {"status": "404", "headers": {}},
                        }
                    }
                ]
            },
            {},
        )
        print(r)
