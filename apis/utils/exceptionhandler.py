import logging
from rest_framework.views import exception_handler
from rest_framework import status
from rest_framework.response import Response
from apis.utils.custom_exceptions import CustomException


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    logging.exception(exc)
    if isinstance(exc, CustomException):
        response = Response(
            {'message': exc.message, 'status_code': exc.status_code,
                'detail': exc.detail},
            status=exc.status_code)
    elif response is not None:
        response.data['status_code'] = response.status_code
    else:
        response = Response(
            {'message': 'Something went wrong. Please try after some time', 'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
             'detail': str(exc) if str(exc) else None}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return response
