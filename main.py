import json
import logging
import os

import requests
from requests.auth import HTTPBasicAuth

from slack_api import Slack

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

domain = os.environ.get("DOMAIN")
bamboo_api_key = os.environ.get("API_KEY")
bamboo_auth = HTTPBasicAuth(bamboo_api_key, "x")
slack_token = os.environ.get('SLACK_API_TOKEN')


def lambda_handler(event, context):
    data = get_bamboo_employees()

    logger.info(data)

    slack_client = Slack(token=slack_token)

    for i in ["jack.popple@infinityworks.com", "will.robinson@infinityworks.com"]:
        slack_client.message_user(i, "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
                                     "Phasellus dignissim massa ac lorem efficitur ultrices. In vitae gravida nibh, "
                                     "sit amet convallis eros."
                                  )

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


    open()

    response.raise_for_status()

    return response.json().get("employees")

