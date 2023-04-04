from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apis.serializers.otp_serializer import OtpSerializer
from apis.database_models.otp_model import OTP
from apis.database_service import otp_service


class OtpView(viewsets.ViewSet):
    query = OTP.objects.all()

    def create(self, request):
        serializer = OtpSerializer(data=request.data)
        if serializer.is_valid():
            otp_data = serializer.validated_data
            response = otp_service.save_otp(otp_data)
            return Response(response, status=200 if response['status'] else 400)
        return Response(serializer.errors, status=400)


@api_view(['POST'])
def validate_otp(request):
    response = otp_service.validate_otp(request.data)
    return Response(response, status=200)
