from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..database_service import bank_name_service
from ..utils import custom_exceptions


@api_view(['GET'])
def all_bank_details_api(req):
    bank_name_data = bank_name_service.bank_name()
    if bank_name_data:
        return Response(bank_name_data, status=status.HTTP_200_OK)
    else:
        raise custom_exceptions.DataNotFoundException(
            "No data found in bank name")


@api_view(['POST'])
def get_bank_id_api(req):
    bank_name = req.data.get('bank_name')
    if not bank_name:
        raise custom_exceptions.DataNotFoundException("bank_name is required")
    bank_name_data = bank_name_service.get_bank_name_service(bank_name)
    if bank_name_data:
        return Response(bank_name_data, status=status.HTTP_200_OK)
    else:
        raise custom_exceptions.DataNotFoundException("No data found in given bank name")
