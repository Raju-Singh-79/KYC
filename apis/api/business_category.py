from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..database_service import business_category_service
from ..utils import custom_exceptions
from apis.utils import Validator


@api_view(['GET'])
def business_category_api(req):
    business_category_data = business_category_service.business_category_details()
    if business_category_data:
        return Response(business_category_data, status=status.HTTP_200_OK)
    else:
        raise custom_exceptions.DataNotFoundException(
            "No data found in business category")


@api_view(['POST'])
def business_category_by_id(req):
    category_id = req.data.get('category_id')
    request_fields = ['category_id']
    Validator.validate_request_data(request_fields, req.data)
    business_category_data = business_category_service.business_category_details_by_id(category_id)
    if business_category_data:
        return Response(business_category_data, status=status.HTTP_200_OK)
    else:
        raise custom_exceptions.DataNotFoundException(
            "No data found in business category")
