from ..configuration.config import Configuration
from apis.utils import custom_exceptions
from apis.database_service import bank_name_service
from apis.utils import Validator
from apis.database_models.mid_creation import MidCreation
from datetime import datetime
from apis.database_service.logger import logger
from apis.utils import generator


def yes_bank_validator(merchant, data):
    client_code = data.get("clientCode")
    payment_mode = data.get("payment_mode")
    bank_name = data.get("bankName")
    sub_merchant_on_boarding_url = Configuration.get_Property("SUB_MERCHANT_ONBOARDING_URL")
    logger(f"creating sub merchant id for url {sub_merchant_on_boarding_url}")
    payload_data = generate_subMerchant_payload_data(merchant, data)
    old_data = check_mid_creation_old_data(client_code, payment_mode, bank_name)
    if old_data is True:
        response = Validator.send_request(sub_merchant_on_boarding_url, payload_data, headers={},
                                          type="POST").json()
        if "subMerchantId" in response and response["subMerchantId"]:
            logger(f"response from bank {response}")
            create_or_update_subMerchant_data(data, response)
            return {"message": "Data Updated", "status": True}
        else:
            logger(
                f"something went wrong, check the data: response from bank: {response} and request body is: {payload_data}")
            raise custom_exceptions.UnauthorizedBankException(
                f"response from bank: {response} and request body is: {payload_data}")


def check_mid_creation_old_data(client_code, payment_mode, bank_name):
    mid_creation = MidCreation.objects.filter(client_code=client_code, bank_id=bank_name,
                                              payment_mode=payment_mode).values()
    if mid_creation:
        first_result = mid_creation[0]
        if first_result['sub_merchant_id'] == "" or first_result['sub_merchant_id'] is None:
            return True
        else:
            logger(f"MID is already created for this client code {client_code}, and bank name {bank_name}, and payment "
                   f"mode {payment_mode}")
            raise custom_exceptions.MidCreation("MID Already Created")
    else:
        return True


def create_or_update_subMerchant_data(data, response):
    try:
        merchant_mid = MidCreation.objects.get(client_code=data.get("clientCode"), bank_id=data.get("bankName"),
                                               payment_mode=data.get("payment_mode"))
    except Exception:
        merchant_mid = MidCreation()
        merchant_mid.created_date = datetime.now()
    merchant_mid.modified_date = datetime.now()
    merchant_mid.client_code = data.get("clientCode")
    merchant_mid.payment_mode = data.get("payment_mode")
    merchant_mid.bank_id = bank_name_service.get_bank_data(data.get("bankName"))
    merchant_mid.response = response
    response_dat = response.get("subMerchantId")
    merchant_mid.sub_merchant_id = response_dat if response_dat and response_dat.strip() else None
    merchant_mid.save()


def generate_subMerchant_payload_data(merchant, data):
    return {
        "bankrequestId": generator.generate_otp(),
        "clientCode": str(data.get("clientCode")),
        "clientId": "123",
        "onboardStatus": "",
        "onboardTime": str(datetime.now().date()),
        "clientName": str(merchant.clientName),
        "clientAddress": str(merchant.operationalAddress),
        "clientBusinessType": "4",
        "clientEmail": str(merchant.emailId),
        "clientMobileNo": str(merchant.contactNumber),
        "clientPanNo": str(merchant.panCard),
        "clientGstNo": str(merchant.gstNumber),
        "clientUrl": "https://sabpaisa.in/",
        "clientPdayTxnCount": "100",
        "clientPdayTxnLmt": "100",
        "clientPdayTxnAmt": "100",
        "udf1": "",
        "udf2": "",
        "udf3": "",
        "udf4": "",
        "udf5": "",
        "udf6": "",
        "udf7": "",
        "udf8": "",
        "udf9": "",
        "udf10": "",
        "paymentMode": str(bank_name_service.get_payment_mode_name(data.get("payment_mode"))),
        "bankName": bank_name_service.bank_name_by_id(data.get("bankName")),
        "clientVirtualAdd": bank_name_service.generate_random_string(10)
    }
