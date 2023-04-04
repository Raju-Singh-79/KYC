from ..serializers.lookup_serializer import BankNameSerializer
from ..database_models.bank_master import bank_master
import traceback
import random
import string
from apis.utils import custom_exceptions
from apis.database_models.lookup_business_type import business_type
from apis.database_models.payement_mode import PaymentMode


def bank_name():
    get_bank_name_data = bank_master.objects.all()
    return BankNameSerializer(get_bank_name_data, many=True).data


def get_bank_name_service(bank_name):
    try:
        bank_name_order = bank_name.lower()
        bank_name_order = bank_name.replace("bank", "").strip()
        bank_data = bank_master.objects.filter(bankName__icontains=bank_name_order)
        return BankNameSerializer(bank_data, many=True).data
    except Exception as e:
        traceback.print_exc()
        return None


def generate_random_string(string_length):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(string_length))


def bank_name_by_id(bank_id):
    try:
        bank_name = bank_master.objects.get(bankId=bank_id).bankName
        return str(bank_name.upper().replace(" ", ""))
    except Exception as e:
        raise custom_exceptions.BankNotFound("Bank Name Not Found")


def get_business_type_id(business_type_name):
    try:
        return business_type.objects.get(businessTypeText=business_type_name).businessTypeId
    except Exception:
        raise custom_exceptions.BusinessTypeDataNotFound("Business type Data not found for this merchant")


def get_payment_mode_name(payment_mode_id):
    try:
        return PaymentMode.objects.get(payment_id=payment_mode_id).payment_mode
    except Exception:
        raise custom_exceptions.DataNotFoundException("Payment Mode Not Found")


def get_bank_data(bank_id):
    try:
        return bank_master.objects.get(bankId=bank_id)
    except Exception:
        raise custom_exceptions.BankNotFound("Bank Name Not Founds")
