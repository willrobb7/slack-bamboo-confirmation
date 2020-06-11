import json
import logging
import os

import requests
from requests.auth import HTTPBasicAuth

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

domain = os.environ.get("DOMAIN")
bamboo_api_key = os.environ.get("API_KEY")
bamboo_auth = HTTPBasicAuth(bamboo_api_key, "x")


def lambda_handler(event, context):
    data = get_bamboo_employees()

    logger.info(data)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }


def get_bamboo_employees():
    response = requests.post(
        url=f"https://api.bamboohr.com/api/gateway.php/{domain}/v1/reports/custom",
        headers={"content-type": "application/json"},
        params={"format": "JSON"},
        data=json.dumps({
            "title": "Work Email pleaz",

            "fields": [
                "status",
                "firstName",
                "middleName",
                "preferredName",
                "lastName",
                "workEmail"
            ]
        }),
        auth=bamboo_auth
    )


    response.raise_for_status()

    return response.json().get("employees")

