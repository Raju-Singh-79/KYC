import traceback
from django.db import models
from django.db.models import F, Value
from django.db.models.functions import Concat
from django.http import JsonResponse
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import timedelta
from apis.utils.custom_exceptions import DataNotFoundException, IncompleteDataException
from ..serializers.client_account_serializer import ClientAccountDetailSerializer
from ..serializers.merchant_serializer import MerchantData, MerchantDocumentById, merchant_data_serializer, \
    MerchantConsent
from ..database_models.merchant_data import merchant_data
from ..database_models.merchant_document import merchant_document
from ..database_service import merchant_data_service, client_account_details_service
from ..utils import PaginationMeta
from ..serializers.merchant_address_serializer import MerchantAddressSerializer
from ..database_models.lookup_state import lookup_state
from ..database_models.kyc_consent import kyc_consent
from datetime import datetime
from ..database_models.verification import Verification
from ..serializers.verification_serializer import VerificationDataSerializer
from django.db.models import Q
from rest_framework.decorators import action
from ..database_models.login_master import login_master
from ..serializers.login_master_serializer import login_master_serializer
import json
from django.http import JsonResponse


class GetMerchantData(APIView):
    def get(self, requset):
        merchant = merchant_data.objects.all().annotate(
            names=Concat(F('name'), Value('::'), F('companyName'), output_field=models.TextField()))
        serialized_data = MerchantData(merchant, many=True)
        return JsonResponse({"data": serialized_data.data}, status=status.HTTP_200_OK)


class GetMerchantDocumentByID(APIView):
    def get(self, request):
        merchant_id = request.GET['Id']
        merchant_doc = merchant_document.objects.filter(merchantId=merchant_id).annotate(
            OriginialFilePath=Concat(Value('https://spl.sabpaisa.in'), F('filePath'), output_field=models.TextField()))
        serialized_data = MerchantDocumentById(merchant_doc, many=True)
        return JsonResponse({"data": serialized_data.data}, status=status.HTTP_200_OK)


@api_view(['POST'])
def merchant_data_by_client_code(req):
    client_code = req.data.get('client_code')
    if not client_code:
        raise DataNotFoundException("client_code is required")
    merchant_data_by_client_code = merchant_data_service.merchant_data_by_client_code(
        client_code)
    if not merchant_data_by_client_code:
        raise DataNotFoundException("Data not found")
    return Response(merchant_data_by_client_code, status=status.HTTP_200_OK)


def get_merchant_consent_by_id(login_id):
    try:
        merchant = kyc_consent.objects.get(login_id=login_id)
        return merchant
    except Exception:
        traceback.print_exc()
        return None


@api_view(['POST'])
def merchant_data_by_login_id(req):
    login_id = req.data.get('login_id')
    if not login_id:
        raise IncompleteDataException("login_id is required")

    merchant_data = merchant_data_service.merchant_data_by_login_id(login_id)
    merchant_data_response = merchant_data_serializer(merchant_data).data

    try:
        try:
            merchant_account_details = client_account_details_service.client_account_details_by_merchant_id(
                merchant_data.merchantId)
            merchant_data_response['merchant_account_details'] = ClientAccountDetailSerializer(
                merchant_account_details).data
        except Exception:
            merchant_data_response['merchant_account_details'] = None
        merchant_address_detail = merchant_data_service.get_merchant_address_by_id(
            login_id)
        merchant_consent = get_merchant_consent_by_id(login_id)
        state_name = None
        try:
            merchant_state = merchant_address_detail.state
            state_name = lookup_state.objects.get(stateId=merchant_state).stateName
        except Exception:
            pass
        merchant_data_response['merchant_address_details'] = MerchantAddressSerializer(
            merchant_address_detail).data
        merchant_data_response['merchant_consent'] = MerchantConsent(merchant_consent).data
        merchant_data_response['merchant_address_details']['state_name'] = state_name

    except Exception:
        traceback.print_exc()
        merchant_data_response['merchant_account_details'] = None
        merchant_data_response['merchant_address_details'] = None
        merchant_data_response['merchant_consent'] = None
    if not merchant_data:
        raise DataNotFoundException("Data not found")
    return Response(merchant_data_response, status=status.HTTP_200_OK)


# class MerchantApi(viewsets.ViewSet):
#     query_set = Verification.objects.all()
#     serializer_class = VerificationDataSerializer

#     def list(self, request):
#         order_by = request.query_params.get('order_by', 'id')
#         search_term = request.query_params.get('search')
#         start_date = request.query_params.get('from_date')
#         end_date = request.query_params.get('to_date')
#         search_map = request.query_params.get("search_map")
#         search_field = "status"
#         if start_date is not None:
#             from_date = datetime.strptime(start_date, '%Y-%m-%d')
#         else:
#             from_date = datetime.min
#         if end_date is not None:
#             to_date = datetime.strptime(end_date, '%Y-%m-%d')
#         else:
#             to_date = datetime.now()
#         if from_date > to_date:
#             return Response({"status": False, "message": "End date can't be before Start date"})
#         verification_queryset = get_verification_data_by_date(from_date, to_date, order_by, search_map)
#         queryset = verification_queryset.filter(**{search_field: search_term})
#         paginator = PaginationMeta.PaginationMeta()
#         page = paginator.paginate_queryset(queryset, request)
#         if page is not None and request.query_params.get("page_size"):
#             serializer = self.serializer_class(page, many=True)
#             response_data = PaginationMeta.get_custom_merchant_response(serializer.data)
#             return paginator.get_paginated_response(response_data)
#         else:
#             serializer = self.serializer_class(queryset, many=True)
#             return Response(PaginationMeta.get_custom_merchant_response(serializer.data))


# def get_verification_data_by_date(from_date, to_date, order_by, search_map):
#     if search_map is not None or "":
#         return Verification.objects.filter(
#             **{f"{search_map}__range": (from_date, to_date + timedelta(days=1))}).order_by(order_by)
#     else:
#         return Verification.objects.all().order_by(order_by)


# class MerchantApi(viewsets.ViewSet):
#     query_set = merchant_data.objects.all()
#     serializer_class = merchant_data_serializer

#     def list(self, request):
#         order_by = request.query_params.get('order_by', 'merchantId')
#         search_term = request.query_params.get('search')
#         start_date = request.query_params.get('from_date')
#         end_date = request.query_params.get('to_date')
#         search_map = request.query_params.get("search_map")
#         search_field = "status"
#         if start_date is not None:
#             from_date = datetime.strptime(start_date, '%Y-%m-%d')
#         else:
#             from_date = datetime.min
#         if end_date is not None:
#             to_date = datetime.strptime(end_date, '%Y-%m-%d')
#         else:
#             to_date = datetime.now()
#         if from_date > to_date:
#             return Response({"status": False, "message": "End date can't be before Start date"})
#         merchant_queryset = get_merchant_data_by_date(from_date, to_date, order_by, search_map)
#         queryset = merchant_queryset.filter(**{search_field: search_term})
#         paginator = PaginationMeta.PaginationMeta()
#         page = paginator.paginate_queryset(queryset, request)
#         if page is not None and request.query_params.get("page_size"):
#             serializer = self.serializer_class(page, many=True)
#             response_data = PaginationMeta.get_custom_merchant_response(serializer.data)
#             return paginator.get_paginated_response(response_data)
#         else:
#             serializer = self.serializer_class(queryset, many=True)
#             return Response(PaginationMeta.get_custom_merchant_response(serializer.data))


# def get_merchant_data_by_date(from_date, to_date, order_by, search_map):
#     merchant = list(merchant_data.objects.filter(status=search_map))
#     print(merchant)
#     for data in merchant:
#         try:
#             ver = Verification.objects.filter(login_id=data.loginMasterId)
#         except:
#             obj = merchant

#     if search_map is not None or "":
#         return merchant_data.objects.filter(
#             **{f"{search_map}__range": (from_date, to_date + timedelta(days=1))}).order_by(order_by)
#     else:
#         return merchant_data.objects.all().order_by(order_by)


# class MerchantApi(viewsets.ViewSet):
#     query_set = Verification.objects.all()
#     serializer_class = VerificationDataSerializer

#     def list(self, request):
#         order_by = request.query_params.get('order_by', 'id')
#         search_term = request.query_params.get('search')
#         start_date = request.query_params.get('from_date')
#         end_date = request.query_params.get('to_date')
#         search_map = request.query_params.get("search_map")
#         search_field = "status"
#         if start_date is not None:
#             from_date = datetime.strptime(start_date, '%Y-%m-%d')
#         else:
#             from_date = datetime.min
#         if end_date is not None:
#             to_date = datetime.strptime(end_date, '%Y-%m-%d')
#         else:
#             to_date = datetime.now()
#         if from_date > to_date:
#             return Response({"status": False, "message": "End date can't be before Start date"})
#         verification_queryset = get_verification_data_by_date(from_date, to_date, order_by, search_map, search_field, search_term)
#         queryset = verification_queryset.filter(**{search_field: search_term})
#         paginator = PaginationMeta.PaginationMeta()
#         page = paginator.paginate_queryset(queryset, request)
#         if page is not None and request.query_params.get("page_size"):
#             serializer = self.serializer_class(page, many=True)
#             response_data = PaginationMeta.get_custom_merchant_response(serializer.data)
#             return paginator.get_paginated_response(response_data)
#         else:
#             serializer = self.serializer_class(queryset, many=True)
#             return Response(PaginationMeta.get_custom_merchant_response(serializer.data))


# def get_verification_data_by_date(from_date, to_date, order_by, search_map, search_field, search_term):
#     merchant = list(merchant_data.objects.filter(**{search_field: search_term}))
#     for data in merchant:
#         try:
#             queryset_obj = Verification.objects.filter(login_id=data.loginMasterId)
#             print(queryset_obj)

#         except:
#             merchant_obj = merchant()
#             print(merchant_obj)

#     if search_map is not None or "":
#         return Verification.objects.filter(
#             **{f"{search_map}__range": (from_date, to_date + timedelta(days=1))}).order_by(order_by)
#     else:
#         return Verification.objects.all().order_by(order_by)


class MerchantApi(viewsets.ViewSet):
    query_set = Verification.objects.all()
    serializer_class = VerificationDataSerializer

    def list(self, request):
        order_by = request.query_params.get('order_by', 'id')
        search_term = request.query_params.get('search')
        start_date = request.query_params.get('from_date')
        end_date = request.query_params.get('to_date')
        search_map = request.query_params.get("search_map")
        search_field = "status"
        if start_date is not None:
            from_date = datetime.strptime(start_date, '%Y-%m-%d')
        else:
            from_date = datetime.min
        if end_date is not None:
            to_date = datetime.strptime(end_date, '%Y-%m-%d')
        else:
            to_date = datetime.now()
        if from_date > to_date:
            return Response({"status": False, "message": "End date can't be before Start date"})
        queryset = get_verification_data_by_date(from_date, to_date, order_by, search_map, search_field, search_term)
        # queryset = verification_queryset.filter(**{search_field: search_term})
        paginator = PaginationMeta.PaginationMeta()
        page = paginator.paginate_queryset(queryset, request)
        if page is not None and request.query_params.get("page_size"):
            serializer = self.serializer_class(page, many=True)
            response_data = PaginationMeta.get_custom_merchant_response(serializer.data)
            return paginator.get_paginated_response(response_data)
        else:
            serializer = self.serializer_class(queryset, many=True)
            return Response(PaginationMeta.get_custom_merchant_response(serializer.data))
        

    # @action(methods=['Get'], detail=False, url_path='offline-data')
    # def MerchantDataApi(self, request):
    #     order_by = request.query_params.get('order_by', 'merchantId')
    #     search_term = request.query_params.get('search')
    #     search_field = "status"
    #     merchant_queryset = merchant_data.objects.filter(**{search_field: search_term}).order_by(order_by)
    #     # print(">>>>>>>>>>>>>>>>merchant_queryset : ", merchant_queryset)
    #     merch = [data.loginMasterId for data in merchant_queryset]
    #     # print(">>>>>>>>>>>>>>>>>>>>>>>>>>> : ", merch)
    #     for data in merchant_queryset:
    #         login_master_data = login_master.objects.filter(isDirect=False)
    #         print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> :", login_master_data)
    #         serializer_data = login_master_serializer(login_master_data, many=True).data
    #         # print(serializer_data)
    #     # return Response (login_master_data)
    #     return Response(serializer_data)


    @action(methods=['Get'], detail=False, url_path='offline-data')
    def MerchantDataApi(self, request):
        order_by = request.query_params.get('order_by', 'merchantId')
        search_term = request.query_params.get('search')
        search_field = "status"
        merchant_queryset = merchant_data.objects.filter(**{search_field: search_term}).order_by(order_by)
        merchant = [data.loginMasterId for data in merchant_queryset]
        login_master_data = login_master.objects.filter(loginMasterId__in=merchant, isDirect=False)
        # print(login_master_data)
        # paginator = PaginationMeta.PaginationMeta()
        # page = paginator.paginate_queryset(login_master_data, request)
        loginid_of_login = {login.loginMasterId: login for login in login_master_data}
        
        merged_data = []

        for data in merchant_queryset:
            print(">>>>>>>>>>>>>>>>>>>>>>>merchant_queryset :", merchant_queryset)
            if data.loginMasterId in loginid_of_login:
                paginator = PaginationMeta.PaginationMeta()
                page = paginator.paginate_queryset(merchant_queryset, request)
                merchant = merchant_data_serializer(page, many=True).data
                # print(merchant)
                response_data = PaginationMeta.get_custom_merchant_response(merchant)
                # print(">>>>>>>>>>>>>>>>>>>response_data :", response_data)
                # merged_data.append(merchant)
                merged_data.append(response_data)
        return Response(merged_data)
    




def get_verification_data_by_date(from_date, to_date, order_by, search_map, search_field, search_term):
    merchantdata = merchant_data.objects.filter(**{search_field: search_term})
    # print(merchantdata)
    # verification_data = Verification.objects.filter(
    #     Q(**{search_map: from_date}) | Q(**{search_map: to_date + timedelta(days=1)}),
    #     ).order_by(order_by)
    verification_data = Verification.objects.filter(
           **{f"{search_map}__range": (from_date, to_date + timedelta(days=1))}).order_by(order_by)
    # print("verification_data>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", verification_data)_
    merchant_login_master_id = [item.loginMasterId for item in merchantdata]
    # print("merchant_login_master_id>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", merchant_login_master_id)
    filtered_verification_data = verification_data.filter(login_id=merchant_login_master_id).first()
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>filtered_verification_data", filtered_verification_data)


    merged_data = []
    for item in merchantdata:
        matching_verification = filtered_verification_data.filter(login_id=item.loginMasterId).first()
        merged_item = {'merchantdata': item, 'verification_data': matching_verification}
        merged_data.append(merged_item)
    return merged_data
    