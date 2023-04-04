import threading
import time
from apis.configuration.config import Configuration
from apis.database_models.login_master import login_master
from apis.database_models.otp_model import OTP
from apis.enums.otpcodes import OtpStatus, OtpType
from apis.utils import Sms, Email
from apis.utils import generator
import requests
import json
import traceback
from apis.database_service.logger import logger


def save_otp(otp):
    if not otp.get("email") and not otp.get("mobile_number"):
        return {"status": False, "message": "Please provide email or mobile number"}
    otp = OTP(**otp)
    otp.otp = generator.generate_otp()
    otp.status = OtpStatus.PENDING.value
    otp.verification_token = generator.generate_verification_token()
    if otp.otp_type.lower() == OtpType.PHONE.value.lower() and otp.mobile_number is not None:
        otp.otp_type = OtpType.PHONE.value
        # logger(f"otp send successfully to mobile number {otp.mobile_number}")
        send_otp_sms(otp.mobile_number, "Your OTP is {} for {}".format(otp.otp, otp.otp_for))
    elif otp.otp_type.lower() == OtpType.EMAIL.value.lower() and otp.email is not None:
        otp.otp_type = OtpType.EMAIL.value
        user_name = login_master.objects.get(email=otp.email).name
        # logger(f"otp send successfully to email id {otp.email}")
        email_otp_validation(otp.email, user_name, otp.otp)
    else:
        logger(f"Invalid OTP type. Valid types are: Phone, Email")
        return {"status": False, "message": "Invalid OTP type. Valid types are: Phone, Email", }
    otp.save()
    expire_otp_thread(otp.id)
    return {"status": True, "verification_token": otp.verification_token}


def expire_otp(otp_id: int):
    otp = OTP.objects.get(id=otp_id)
    if otp.status == OtpStatus.PENDING.value:
        otp.is_expired = True
        otp.status = OtpStatus.EXPIRED.value
        otp.save()
    return {"status": True}


def expire_otp_thread(otp_id: int):
    otp_expire_time = Configuration.get_Property("OTP_EXPIRE_TIME")

    class expire_otp_inner_thread(threading.Thread):
        def __init__(self, otp_id):
            threading.Thread.__init__(self)
            self.otp_id = otp_id

        def run(self):
            time.sleep(60 * int(otp_expire_time))
            expire_otp(self.otp_id)

    expire_otp_inner_thread(otp_id).start()


def send_otp_sms(mobile_number: str, message: str):
    Sms.sms_thread(mobile_number, message)


def send_otp_email(to: str, subject: str, message: str):
    Email.email_thread(to, subject, message)


def validate_otp(otp_data):
    otp = otp_data.get("otp")
    verification_token = otp_data.get("verification_token")
    if not otp or not verification_token:
        return {"status": False, "message": "Invalid OTP data"}
    try:
        otp = OTP.objects.get(verification_token=otp_data["verification_token"], otp=otp_data["otp"])
        if otp.is_expired:
            logger(f"otp is expired for:  {otp.mobile_number}")
            return {"status": False, "message": "OTP is expired"}
        if otp.status == OtpStatus.VERIFIED.value:
            return {"status": False, "message": "OTP is already verified"}
        else:
            otp.status = OtpStatus.VERIFIED.value
            otp.save()
            return {"status": True, "message": "OTP verified successfully"}
    except OTP.DoesNotExist:
        logger(f"invalid otp {otp.mobile_number}")
        return {"status": False, "message": "Invalid OTP"}


def otp_by_phone(mobile_number):
    otp_list = OTP.objects.filter(
        mobile_number=mobile_number,
        status=OtpStatus.VERIFIED.value,
        otp_type=OtpType.PHONE.value,
    )
    if len(otp_list) > 0:
        return otp_list.first()
    else:
        return None


def otp_by_email(email_id):
    otp_list = OTP.objects.filter(
        email=email_id, status=OtpStatus.VERIFIED.value, otp_type=OtpType.EMAIL.value
    )
    if len(otp_list) > 0:
        return otp_list.first()
    else:
        return None


def email_otp_validation(to, user_name, otp):
    try:
        mail_api = Configuration.get_Property("EMAIL_API_MSG91")
        headers = Email.email_api_msg91_headers
        payload_data = Email.send_email_msg91_payload(to, "cob-sabpaisa", "KYC", user_name, otp)
        mail_response = requests.post(mail_api, data=json.dumps(payload_data), headers=headers)
        response_mail_data = mail_response.json().get("data")
        print("email response data :", response_mail_data)
        print("email send at:", to)
        if response_mail_data is None:
            send_otp_email(to, "OTP for KYC SabPaisa", "Your OTP for KYC: {}".format(otp))
    except Exception:
        traceback.print_exc()
