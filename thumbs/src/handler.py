import base64
from io import BytesIO
from os.path import basename, dirname, splitext, sep
from os import makedirs
import re
import sys
from typing import Tuple
from urllib.parse import unquote

import boto3

import django
from django.conf import settings

settings.configure(THUMBNAIL_KVSTORE="thumbs.PassthruKVStore",)
django.setup()

from PIL import Image, ImageOps
from sorl.thumbnail import get_thumbnail
from sorl.thumbnail import conf as sorl_conf
from sorl.thumbnail.base import ThumbnailBackend
from sorl.thumbnail.engines import pil_engine
from sorl.thumbnail.parsers import parse_crop, parse_geometry


client = boto3.client("s3")
engine = pil_engine.Engine()


def handle(event, context):
    if "s3" in event["Records"][0]:
        return handle_s3(event, context)
    elif "cf" in event["Records"][0]:
        return handle_cf(event, context)


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

    path = sep.join(parts)

    image = fetch_image("data.electionleaflets.org", path)
    processed = process_image(image, (size, options))
    key = new_key((size, options), path)
    upload_image(processed, image.format, "data.electionleaflets.org", key)

    io = BytesIO()
    processed.save(io, image.format)

    response["headers"]["content-type"] = [
        {"key": "Content-Type", "value": Image.MIME[image.format]}
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

        image = fetch_image(r["s3"]["bucket"]["name"], r["s3"]["object"]["key"])

        for spec in SPECS:
            processed = process_image(image, spec)
            key = new_key(spec, r["s3"]["object"]["key"])
            upload_image(
                processed, image.format, r["s3"]["bucket"]["name"], key, local
            )


def fetch_image(bucket: str, key: str):
    print(key)
    response = client.get_object(Bucket=bucket, Key=key)

    return Image.open(response["Body"])


def new_key(spec: tuple, key: str) -> str:
    size = spec[0]
    options = spec[1]

    option_parts = [str(size)]
    option_parts.extend(sorted(["=".join(o) for o in list(options.items())]))

    return "thumbs/{}/{}".format("/".join(option_parts), key)


def process_image(image: Image, spec: Tuple[str, dict]) -> Image:
    size = spec[0]
    options = spec[1].copy()

    for key, value in list(ThumbnailBackend.default_options.items()):
        options.setdefault(key, value)

    ratio = engine.get_image_ratio(image, options)
    geometry = parse_geometry(size, ratio)
    return engine.create(image, geometry, options)


def upload_image(
    image: Image, format: str, bucket: str, key: str, local: bool = False
):
    io = BytesIO()
    image.save(io, format)
    if local:
        makedirs(dirname(key), exist_ok=True)
        image.save(key, format)

    client.put_object(
        ACL="public-read",
        Body=io.getvalue(),
        Bucket=bucket,
        Key=key,
        ContentType=Image.MIME[format],
    )


if __name__ == "__main__":
    if sys.argv[1] == "--s3":
        handle_s3(
            {
                "Records": [
                    {
                        "s3": {
                            "bucket": {"name": "data.electionleaflets.org"},
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
