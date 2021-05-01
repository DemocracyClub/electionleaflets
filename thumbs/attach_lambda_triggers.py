import os

import boto3
from botocore.exceptions import BotoCoreError

IMAGES_BUCKET_NAME = os.environ.get("LEAFLET_IMAGES_BUCKET_NAME")
IMAGES_URL = f"images.{os.environ.get('PUBLIC_FQDN')}"
ENVIRONMENT = os.environ.get("SAM_LAMBDA_CONFIG_ENV")

s3_client = boto3.client("s3", "eu-west-2")
lambda_client = boto3.client("lambda", "eu-west-2")


def get_thumbs_function(lambda_client):
    for function in lambda_client.list_functions()["Functions"]:
        if function["FunctionName"].startswith(
            f"ElectionLeafletsThumbs-{ENVIRONMENT}"
        ):
            return function


def policy_exists(arn):
    try:
        policy = lambda_client.get_policy(FunctionName=function_arn)
    except:
        return False
    return "s3_thumbs" in policy["Policy"]


lambda_function = get_thumbs_function(lambda_client)
function_arn = lambda_function["FunctionArn"]
if not policy_exists(function_arn):
    lambda_client.add_permission(
        FunctionName=function_arn,
        StatementId="s3_thumbs",
        Action="lambda:InvokeFunction",
        Principal="s3.amazonaws.com",
    )

response = s3_client.put_bucket_notification_configuration(
    Bucket=IMAGES_BUCKET_NAME,
    NotificationConfiguration={
        "LambdaFunctionConfigurations": [
            {
                "Id": "ImageResizer",
                "LambdaFunctionArn": function_arn,
                "Events": ["s3:ObjectCreated:*"],
                "Filter": {
                    "Key": {
                        "FilterRules": [
                            {"Name": "prefix", "Value": "leaflets/",},
                            {"Name": "Suffix", "Value": ""},
                        ]
                    }
                },
            }
        ]
    },
)

cf_client = boto3.client("cloudfront")
lambda_client_us = boto3.client("lambda", "us-east-1")
lambda_function_us = get_thumbs_function(lambda_client_us)


def get_dist(cf_client):
    for dist in cf_client.list_distributions()["DistributionList"]["Items"]:
        if IMAGES_URL in dist["Aliases"]["Items"]:
            return dist


dist = get_dist(cf_client)
version = lambda_client_us.publish_version(
    FunctionName=lambda_function_us["FunctionName"]
)
version_arn = version["FunctionArn"]
config = cf_client.get_distribution_config(Id=dist["Id"])
config["DistributionConfig"]["CacheBehaviors"]["Items"][0][
    "LambdaFunctionAssociations"
] = {
    "Quantity": 1,
    "Items": [
        {
            "LambdaFunctionARN": version_arn,
            "EventType": "origin-response",
            "IncludeBody": False,
        }
    ],
}
cf_client.update_distribution(
    DistributionConfig=config["DistributionConfig"],
    Id=dist["Id"],
    IfMatch=config["ETag"],
)
