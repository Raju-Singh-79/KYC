from rest_framework import status, viewsets
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from apis.utils import Validator
from apis.database_service import mid_creation_service
from apis.database_service import merchant_data_service
from apis.database_models.mid_creation import MidCreation
from ..utils.PaginationMeta import PaginationMeta
from apis.serializers import mid_creation_serializer


class SubMerchantMidCreation(viewsets.ViewSet):
    queryset = MidCreation.objects.all()

    @action(detail=False, methods=["post"], url_path="send-request-subMerchant-mid")
    def send_request_subMerchant_mid(self, request):
        data = request.data
        clientCode = data.get("clientCode")
        request_fields = ["clientCode", "bankName"]
        Validator.validate_request_data(request_fields, request.data)
        merchant = merchant_data_service.merchantData_by_client_code(data.get("clientCode"))
        response = mid_creation_service.validate_sub_merchant_id_by_bank(merchant, data)
        if response:
            return Response({"ResponseData": f"Sub Merchant ID Created for {response}", "status_code": 200},
                            status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_path="get-merchant-mid-data")
    def get_merchant_mid_data(self, req):
        clientCode = req.query_params.get("clientCode")
        order_by = req.query_params.get("order_by", "id")
        query_set = self.queryset.filter(client_code=clientCode, is_active=True).order_by(order_by)
        paginator = mid_creation_service.PaginationMeta()
        page = paginator.paginate_queryset(query_set, req)
        if page is not None:
            serializer = mid_creation_serializer.MIDCreationSerializer(page, many=True)
            response_data = paginator.get_custom_paginated_res(serializer.data)
            return response_data
        else:
            serializer = mid_creation_serializer.MIDCreationSerializer(query_set, many=True)
            return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="get-payment-mode-type")
    def get_sub_merchant_data(self, req):
        data = mid_creation_service.get_payment_mode_data()
        return Response({"PaymentModeData": data, "status_code": 200},
                        status=status.HTTP_200_OK)
