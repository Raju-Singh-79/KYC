from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..database_service import collection_frequency_service


@api_view(['GET'])
def collection_frequency_api(req):
    collection_frequency_data = collection_frequency_service.collection_frequency_service()
    if collection_frequency_data:
        return Response(collection_frequency_data, status=status.HTTP_200_OK)
