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
slack_token = os.environ.get('SLACK_TOKEN')

# with statement is a context manager
message_format = None
with open("message_format.json", "r") as json_file:
    message_format = json.loads(json_file.read())


def lambda_handler(event, context):
    data = get_bamboo_employees()

    process_employees(data)
    logger.info(data)

    slack_client = Slack(token=slack_token)

    for i in ["jack.popple@infinityworks.com", "will.robinson@infinityworks.com"]:
        slack_client.message_user(i, "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
                                     "Phasellus dignissim massa ac lorem efficitur ultrices. In vitae gravida nibh, "
                                     "sit amet convallis eros."
                                  )

    return {
        'statusCode': 200,
        'body': json.dumps('All Good!')
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
                "preferredName",
                "lastName",
                "workEmail",
                "address1",
                "address2",
                "zipcode"
            ]
        }),
        auth=bamboo_auth
    )


    response.raise_for_status()

    return response.json().get("employees")


def process_employees(employees: dict):
    for employee in employees:
        status = employee.get("status")
        if status.lower() != "active":
            continue
        print((employee))

        #TODO: Create nice message ready for sending (done)
