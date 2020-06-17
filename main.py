import json
import logging
import os
import urllib
from typing import List

import requests
from requests.auth import HTTPBasicAuth

from slack_api import Slack

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

bamboo_domain = os.environ.get("BAMBOO_DOMAIN")

bamboo_reports_url = f"https://api.bamboohr.com/api/gateway.php/{bamboo_domain}/v1/reports/custom"
bamboo_api_key = os.environ.get("BAMBOO_API_KEY")
bamboo_auth = HTTPBasicAuth(bamboo_api_key, "x")

slack_token = os.environ.get('SLACK_TOKEN')

# with statement is a context manager
with open("message_format.json", "r") as json_file:
    message_format = json.loads(json_file.read())


def process_event(event):
    params = urllib.parse.unquote_plus(urllib.parse.unquote_plus(event['body']))
    params = json.dumps(params)[9:][:-1].replace("\\", "")
    params = json.loads(params)

    return params


# Todo: rename below function/ recreate Lambda with new name
def debug_function(event: dict, context):  # Callback Lambda
    payload: dict = process_event(event)

    response_url = payload.get("response_url")
    actions: dict = payload.get("actions")[0]
    selected_option = actions.get("selected_option")

    logger.info(payload)
    logger.info(selected_option)

    response = determine_callback_response(selected_option.get("value"))

    requests.post(
        response_url,
        data=json.dumps({
            "text": response
        })
    )

    return {
        'statusCode': 200,
        'body': "All good"
    }


def slack_bamboo_confirmation(event, context):  # Initiating Lambda
    bamboo_data = get_bamboo_employees()

    # process_employees()
    incoming_data = json.loads(event.get("body"))

    users_to_message = process_incoming_data(incoming_data, bamboo_data)

    process_employees(users_to_message)

    logger.info(users_to_message)

    return {
        'statusCode': 200,
        'body': json.dumps('All Good!')
    }


def process_incoming_data(data: List[dict], bamboo_data: dict):
    emails = list()

    for employee in data:
        name = employee.get("Individual")

        for bamboo_employee in bamboo_data:
            if bamboo_employee.get("status").lower() != "active":
                logger.info(f"Skipping bamboo user {bamboo_employee} due to being inactive")
                continue

            surname = bamboo_employee.get("lastName")
            preferred_name = bamboo_employee.get('preferredName')

            full_preferred_name = None
            full_name = f"{bamboo_employee.get('firstName')} {surname}".lower()

            if preferred_name:  # Checking preferred_name is not None
                full_preferred_name = f"{preferred_name} {surname}".lower()

            if name.lower() == full_name or name.lower() == full_preferred_name:
                email = bamboo_employee.get("workEmail")
                logger.info(f"Appending {bamboo_employee}")

                emails.append(email)

    return set(emails)


def get_bamboo_employees():
    response = requests.post(
        url=bamboo_reports_url,
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


def get_email_from_bamboo_data():
    pass


def determine_callback_response(selected_option: str):
    user_ref = "<@UN9RPQM88>"  # References Will Robinson on Slack

    if selected_option == "yes":
        return "Thank you, we will be sending asset sticker(s) for your device(s) shortly"

    elif selected_option == "no":
        return f"Thank you, please would you be able to update it on BambooHR and notify {user_ref}"

    elif selected_option == "elsewhere":
        return f"Thank you, please would you be able to message {user_ref} the address you would like " \
               "the asset stickers sent to."


def process_employees(employees: set):
    slack_client = Slack(token=slack_token)

    for employee in employees:
        # status = employee.get("status")
        # email = employee.get("workEmail")

        # if status.lower() != "active" or not email:  # Checks if user is inactive or has a missing workEmail (== None)
        #     logger.info(f"Skipping {employee}")
        #     continue

        logger.info(f"Should be messaging {employee}")
        # slack_client.message_user(email, "Is your address correct in BambooHR?", blocks=message_format)
