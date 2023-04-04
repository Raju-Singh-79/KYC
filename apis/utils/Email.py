import threading

import requests
from apis.configuration.config import Configuration


def send_email(to_email, subject, message):
    mail_api = Configuration.get_Property("MAIL_API")
    headers = {
        "user-agent": "Application",
        "Accept": "*/*",
        "Content-Type": "application/json; charset=utf-8",
    }

    mail_data = {"toEmail": to_email, "toCc": "", "subject": subject, "msg": message}

    response = requests.post(url=mail_api, headers=headers, json=mail_data)
    print(
        "Email to {} sent successfully with subject {} and message {} and response {}".format(
            to_email, subject, message, response.text
        )
    )


def email_thread(to_email, subject, message):
    thread = threading.Thread(target=send_email, args=(to_email, subject, message))
    thread.start()


email_api_msg91_headers = {
    "Content-Type": "application/JSON",
    "Accept": "application/json",
    "authkey": "375106ATCatDUwIZ26305eba8P1",
}


def send_email_msg91_payload(to, template_id, variable1, variable2, variable3):
    payload = {
        "to": [{"name": "", "email": to}],
        "from": {"name": "SabPaisa", "email": "noreply@mail.sabpaisa.in"},
        "cc": [],
        "bcc": [],
        "domain": "mail.sabpaisa.in",
        "mail_type_id": "3",
        "template_id": template_id,
        "variables": {"VAR1": variable1, "VAR2": variable2, "VAR3": variable3},
    }
    return payload


def send_email_kyc_merchant_payload(to, template_id, variable1, variable2):
    payload = {
        "to": [{"name": "", "email": to}],
        "from": {"name": "SabPaisa", "email": "noreply@mail.sabpaisa.in"},
        "cc": [],
        "bcc": [],
        "domain": "mail.sabpaisa.in",
        "mail_type_id": "3",
        "template_id": template_id,
        "variables": {"VAR1": variable1, "VAR2": variable2},
    }
    return payload