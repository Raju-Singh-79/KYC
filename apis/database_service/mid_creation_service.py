from apis.database_models.merchant_data import merchant_data
from apis.utils import custom_exceptions
from apis.database_service import bank_name_service
from apis.database_models.mid_creation import MidCreation
from apis.enums.midcreation import MIDName
from apis.database_models.payement_mode import PaymentMode
from apis.serializers import mid_creation_serializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict
from apis.database_service.logger import logger
from apis.bank_service import mid_yes_bank


def validate_sub_merchant_id_by_bank(merchant: merchant_data, data):
    bank_name = data.get("bankName")
    bank_data = bank_name_service.get_bank_data(bank_name)
    if bank_data.bankName == MIDName.YESBANK.value:
        validate_yes_bank = mid_yes_bank.yes_bank_validator(merchant, data)
        return bank_data.bankName
    else:
        logger(f"Bank is not register for creating mid of bank name {bank_name}")
        raise custom_exceptions.BankNotIntegrated("Bank is not register, contact to administrator")


def get_mid_data(client_code):
    return MidCreation.objects.get(client_code=client_code)


def get_payment_mode_data():
    payment_mode = PaymentMode.objects.all()
    return mid_creation_serializer.PaymentModeSerializer(payment_mode, many=True).data


class PaginationMeta(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 10000

    def get_custom_paginated_res(self, data):
        for merchant in data:
            merchant_list = list(merchant.values())
            client_code = merchant_list[1]
            payment_mode = merchant_list[2]
            bank_id = merchant_list[7]
            try:
                payment_mode = PaymentMode.objects.get(payment_id=payment_mode).payment_mode
            except Exception:
                payment_mode = None
            try:
                bank_name = bank_name_service.get_bank_data(bank_id).bankName
            except Exception:
                bank_name = None
            merchant.update({"PaymentMode": payment_mode})
            merchant.update({"BankName": bank_name})

        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('MidData', data)
        ]))
