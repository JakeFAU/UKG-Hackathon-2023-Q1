import json

# import requests


def lambda_handler(event, context):
    """Sample pure Lambda function"""

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": "I'm Ok",
            }
        ),
    }
