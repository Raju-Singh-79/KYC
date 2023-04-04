from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..database_service import platform_service
from ..utils import custom_exceptions


@api_view(['GET'])
def platform_type_api(req):
    platform_type_data = platform_service.platform_data()
    if platform_type_data:
        return Response(platform_type_data, status=status.HTTP_200_OK)
    else:
        raise custom_exceptions.DataNotFoundException(
            "No data found in platform type")
