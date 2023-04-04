from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..database_service import role_service
from ..utils import custom_exceptions


@api_view(['GET'])
def role_data_api(req):
    role_type_data = role_service.get_role_id_and_name(req)
    if role_type_data:
        return Response(role_type_data, status=status.HTTP_200_OK)
    else:
        raise custom_exceptions.DataNotFoundException(
            "No data found in role type")


@api_view(['GET'])
def risk_category_data_api(req):
    risk_type_data = role_service.get_risk_category_data(req)
    if risk_type_data:
        return Response(risk_type_data, status=status.HTTP_200_OK)
    else:
        raise custom_exceptions.DataNotFoundException(
            "No data found")
