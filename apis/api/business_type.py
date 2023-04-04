from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..database_service import business_type_service
from ..utils import custom_exceptions
from apis.utils import Validator

@api_view(['GET'])
def business_type_api(req):
    business_type_data = business_type_service.business_type_details()
    if business_type_data:
        return Response(business_type_data, status=status.HTTP_200_OK)
    else:
        raise custom_exceptions.DataNotFoundException(
            "No data found in business type")


@api_view(['POST'])
def business_type_by_id(req):
    business_type_id = req.data.get('business_type_id')
    request_fields = ['business_type_id']
    Validator.validate_request_data(request_fields, req.data)
    business_type_data = business_type_service.business_type_details_by_id(business_type_id)
    if business_type_data:
        return Response(business_type_data, status=status.HTTP_200_OK)
    else:
        raise custom_exceptions.DataNotFoundException(
            "No data found in business type")