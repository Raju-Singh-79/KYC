from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..database_service import client_account_details_service


@api_view(['POST'])
def client_account_details(req):
    client_account_details_response = client_account_details_service.get_client_account_details(
        req.data)
    if client_account_details_response:
        return Response(client_account_details_response, status=status.HTTP_200_OK)
