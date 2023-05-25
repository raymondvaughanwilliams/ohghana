import os

import requests


def notify_slack(message: str):
    """Sends message to Slack"""
    payload = {"text": message}
    response = requests.post(url=os.getenv('SLACK_WEBHOOK'), json=payload)
    print(response)


def send_sms(recipient, message):
