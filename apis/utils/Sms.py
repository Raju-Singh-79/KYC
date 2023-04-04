import threading

import requests
from apis.configuration.config import Configuration


def send_sms(phone_number, message):
    sms_api = Configuration.get_Property("SMS_API")
    sender = "SPTRAN"
    route = "4"
    mobiles = phone_number
    message = "Dear , " + message + " -SabPaisa"
    authkey = "177009ASboH8XM59ce18cb"
    DLT_TE_ID = "1107165935399038199"
    country = "91"
    response = requests.post(url=sms_api, params={"sender": sender, "route": route, "mobiles": mobiles,
                                                  "authkey": authkey, "message": message, "DLT_TE_ID": DLT_TE_ID,
                                                  "country": country})

    print("Message to {} sent successfully with the message {} and the response from sms api is {}.".format(
        phone_number, message, response.text))


def sms_thread(phone_number, message):
    thread = threading.Thread(target=send_sms, args=(phone_number, message))
    thread.start()


# send_sms('9540514993', 'Your OTP for kyc1 is 779718 Thanks. Sabpaisa')
