def lambda_handler(event, context):
    headers = event.get("headers", {})
    auth = headers.get("Authorization")
    dc_auth = "Basic ZGM6ZGM="  # dc:dc in base64

    if auth == dc_auth:
        return {
            "principalId": "dc",
            "policyDocument": {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Action": "execute-api:Invoke",
                        "Effect": "Allow",
                        "Resource": "*",
                    }
                ],
            },
        }

    raise Exception("Unauthorized")
