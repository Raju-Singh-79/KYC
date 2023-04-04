from apis.configuration.config import Configuration
from apis.utils import Email
import traceback
import requests
import json
from ..database_service.otp_service import send_otp_email
from ..configuration.config import Configuration

mail_api = Configuration.get_Property("EMAIL_API_MSG91")
headers = Email.email_api_msg91_headers


def email_validation(to, subject, emp_name, user_name, cond1, cond2, user_email, mobile_number):
    try:
        payload_data = send_email_msg91_payload(to, "kyc-approving", subject, emp_name, user_name, cond1, cond2,
                                                user_email, mobile_number)
        mail_response = requests.post(mail_api, data=json.dumps(payload_data), headers=headers)
        response_mail_data = mail_response.json().get("data")
        # print("email response data :", response_mail_data)
        print("email send at:", to)
        if response_mail_data is None:
            send_otp_email(to, f"{subject} KYC Details",
                           f"Dear {emp_name}, {user_name} has been {cond1}, Please {cond2} this Merchant.")
    except Exception:
        traceback.print_exc()


def email_merchant_validation(to, template_name, var1, var2):
    try:
        payload_data = Email.send_email_kyc_merchant_payload(to, template_name, var1, var2)
        mail_response = requests.post(mail_api, data=json.dumps(payload_data), headers=headers)
        response_mail_data = mail_response.json().get("data")
        # print("email response data :", response_mail_data)
        print("email send at:", to)
        if response_mail_data is None:
            send_otp_email(to, f"Your KYC has been approved",
                           f"Dear {var2} We have approved your KYC details & documents")
    except Exception:
        traceback.print_exc()


def send_email_msg91_payload(to, template_id, variable1, variable2, variable3, variable4, variable5, variable6,
                             variable7):
    payload = {
        "to": [{"name": "", "email": to}],
        "from": {"name": "SabPaisa", "email": "noreply@mail.sabpaisa.in"},
        "cc": [],
        "bcc": [],
        "domain": "mail.sabpaisa.in",
        "mail_type_id": "3",
        "template_id": template_id,
        "variables": {"VAR1": variable1, "VAR2": variable2, "VAR3": variable3, "VAR4": variable4, "VAR5": variable5,
                      "VAR6": variable6, "VAR7": variable7},
    }
    print("email send success")
    return payload


def email_kyc_reject_validation(to, template_name, var1, var2):
    try:
        payload_data = Email.send_email_msg91_payload(to, template_name, var1, var2,
                                                      Configuration.get_Property("INTEGRATION_SUPPORT"))
        mail_response = requests.post(mail_api, data=json.dumps(payload_data), headers=headers)
        response_mail_data = mail_response.json().get("data")
        # print("email response data :", response_mail_data)
        print("email send at:", to)
        if response_mail_data is None:
            send_otp_email(to, f"Your KYC is Rejected", f"Your {var1} Data is Rejected.")
    except Exception:
        traceback.print_exc()


def email_reminder_validation(to, subject, variable1, variable2, variable3, variable4, variable5, variable6,
                              variable7):
    try:
        payload_data = send_email_msg91_payload(to, subject, variable1, variable2, variable3, variable4, variable5,
                                                variable6, variable7)
        mail_response = requests.post(mail_api, data=json.dumps(payload_data), headers=headers)
        response_mail_data = mail_response.json().get("data")
        # print("email response data :", response_mail_data)
        print("email send at:", to)
    except Exception:
        traceback.print_exc()
