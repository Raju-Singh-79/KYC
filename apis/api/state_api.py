from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..database_service import state_service
from ..utils import custom_exceptions


@api_view(['POST'])
def state_details_api(req):
    state_data = state_service.all_state_service()
    if state_data:
        return Response(state_data, status=status.HTTP_200_OK)
    else:
        raise custom_exceptions.DataNotFoundException("No data found in state")
