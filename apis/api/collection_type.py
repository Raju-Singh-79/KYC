from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..database_service import collection_type_service
from ..utils import custom_exceptions


@api_view(['GET'])
def collection_type_api(req):
    collection_type_data = collection_type_service.collection_type_data()
    if collection_type_data:
        return Response(collection_type_data, status=status.HTTP_200_OK)
    else:
        raise custom_exceptions.DataNotFoundException(
            "No data found in collection type")
