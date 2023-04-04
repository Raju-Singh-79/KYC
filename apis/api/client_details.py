from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..database_service import client_super_master_service


@api_view(['GET'])
def client_super_master(req):
    client_data = client_super_master_service.all_client_code()
    return Response({"client_code": client_data}, status=status.HTTP_200_OK)
