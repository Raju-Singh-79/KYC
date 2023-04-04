import os

from django.db import transaction
from django.http import Http404, StreamingHttpResponse
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response

from apis.serializers.merchant_document_serializer import MerchantDocumentSerializer, MerchantAadharSerializer
from apis.database_models.merchant_document import merchant_document
from apis.database_service import merchant_document_service, merchant_data_service, role_service
from apis.enums.rolecodes import Role
from apis.utils.PaginationMeta import PaginationMeta
from apis.utils.custom_exceptions import IncompleteDataException, UnauthorizedException
from apis.database_service.logger import logger


class MerchantDocumentAPI(viewsets.ViewSet):
    query = merchant_document.objects.all()

    def create(self, request):
        serializer = MerchantDocumentSerializer(data=request.data)
        if serializer.is_valid():
            merchant_document_data = serializer.validated_data
            response = merchant_document_service.save_merchant_document(
                merchant_document_data)
            return Response(response, status=200 if response['status'] else 400)
        return Response(serializer.errors, status=400)

    @transaction.atomic
    @action(methods=['post'], detail=False, url_path='aadhar-upload')
    def aadhar_upload(self, request):
        try:
            serializer = MerchantAadharSerializer(data=request.data)
            if serializer.is_valid():
                merchant_document_data = serializer.validated_data
                doc_id_list = []
                file_number = 0
                for aadhar in [merchant_document_data['aadhar_front'], merchant_document_data['aadhar_back']]:
                    merchant_document_data['files'] = aadhar
                    merchant_document_data['file_number'] = file_number
                    doc = merchant_document_service.save_merchant_aadhar(merchant_document_data)
                    doc_id_list.append(doc.documentId)
                    file_number += 1
                old_docs = merchant_document.objects.filter(merchant=doc.merchant.merchantId,
                                                            type=merchant_document_data['type'].id).exclude(
                    documentId__in=doc_id_list)
                if old_docs.exists():
                    old_docs.update(isLatest=False)
                return Response({"message": "Merchant document saved successfully", "status": True},
                                status=status.HTTP_200_OK)
            return Response(serializer.errors, status=400)
        except Exception as e:
            transaction.set_rollback(True)
            raise Exception(e)

    def list(self, request):
        order_by = request.query_params.get('order_by', 'documentId')
        queryset = merchant_document.objects.all().order_by(order_by)
        paginator = PaginationMeta()
        page = paginator.paginate_queryset(queryset, request)
        if page is not None:
            serializer = MerchantDocumentSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        else:
            serializer = MerchantDocumentSerializer(queryset, many=True)
            return Response(serializer.data)

    @action(methods=['put'], detail=False, url_path='verify')
    def verify(self, request):
        document_id = request.data.get('document_id')
        verified_by = request.data.get('verified_by')
        if not document_id or not verified_by:
            raise IncompleteDataException("Please provide document_id and verified_by")
        allowed_roles = [Role.VERIFIER.value, Role.APPROVER.value]
        verifier_role = role_service.get_role_by_login_id(verified_by)
        check_access_response = role_service.check_role_access(verifier_role, allowed_roles)
        if not check_access_response:
            raise UnauthorizedException("You are not authorized to perform this action")
        response = None
        for doc_id in document_id:
            response = merchant_document_service.verify_merchant_document(doc_id, verified_by)
            logger(f"Merchant document verified successfully by {verified_by} of merchant doc: {document_id}")
        return Response(response, status=200)

    @action(methods=['put'], detail=False, url_path='approve')
    def approve(self, request):
        document_id = request.data.get('document_id')
        approved_by = request.data.get('approved_by')
        if not document_id or not approved_by:
            raise IncompleteDataException("Please provide document_id and approved_by")
        allowed_roles = [Role.APPROVER.value]
        verifier_role = role_service.get_role_by_login_id(approved_by)
        check_access_response = role_service.check_role_access(verifier_role, allowed_roles)
        if not check_access_response:
            raise UnauthorizedException("You are not authorized to perform this action")
        response = None
        for doc_id in document_id:
            response = merchant_document_service.approve_merchant_document(doc_id, approved_by)
            logger(f"Merchant document approved successfully by {approved_by} of merchant doc: {document_id}")
        return Response(response, status=200)

    @action(methods=['put'], detail=False, url_path='document-reject')
    def doc_reject(self, request):
        document_id = request.data.get('document_id')
        rejected_by = request.data.get('rejected_by')
        comment = request.data.get('comment')
        response = None
        if not document_id or not rejected_by:
            raise IncompleteDataException("Please provide document_id and rejected_by")
        for doc_id in document_id:
            response = merchant_document_service.reject_merchant_document(doc_id, rejected_by, comment)
            logger(f"Merchant document reject because {comment} by {rejected_by} of merchant doc: {document_id}")
        return Response(response, status=200)

    @action(methods=['put'], detail=False, url_path='reject')
    def reject(self, request):
        document_id = request.data.get('document_id')
        rejected_by = request.data.get('rejected_by')
        comment = request.data.get('comment')
        if not document_id or not rejected_by:
            raise IncompleteDataException("Please provide document_id and rejected_by")
        response = merchant_document_service.reject_merchant_document(document_id, rejected_by, comment)
        logger(f"Merchant document reject because {comment} by {rejected_by} of merchant doc: {document_id}")
        return Response(response, status=200)

    @action(methods=['put'], detail=False, url_path='remove')
    def remove(self, request):
        document_id = request.data.get('document_id')
        removed_by = request.data.get('removed_by')
        if not document_id or not removed_by:
            raise IncompleteDataException(
                "Please provide document_id and removed_by")
        response = merchant_document_service.remove_merchant_document(
            document_id, removed_by)
        logger(f"Merchant document remove by {removed_by} of merchant doc: {document_id}")
        return Response(response, status=200)

    @action(detail=False, methods=['post'], url_path='single-file')
    def single_document(self, request):
        serializer = MerchantDocumentSerializer(data=request.data)
        if serializer.is_valid():
            merchant_document_data = serializer.validated_data
            response = merchant_document_service.save_single_merchant_document(
                merchant_document_data)
            return Response(response, status=200 if response['status'] else 400)
        return Response(serializer.errors, status=400)

    @action(detail=False, methods=['post'], url_path='document-by-login-id')
    def document_by_login_id(self, request):
        login_id = request.data.get('login_id')
        if not login_id:
            raise IncompleteDataException("Please provide login_id")
        doc_list = merchant_document_service.get_merchant_document_by_login_id(
            login_id)
        response = MerchantDocumentSerializer(doc_list, many=True).data
        return Response(response, status=200)


@api_view(['GET'])
def get_merchant_doc(request):
    document_id = request.query_params.get('document_id')
    download = request.query_params.get('download')
    file_path = merchant_document_service.get_document_path_by_id(document_id)
    if file_path is None:
        raise Http404
    complete_file_path = os.getcwd() + "/" + file_path.filePath
    if os.path.exists(complete_file_path):
        resp = StreamingHttpResponse(
            streaming_content=open(complete_file_path, 'rb'))
        file_name = file_path.filePath.split("/")[-1]
        file_extension = file_name.split(".")[-1]
        if file_extension == "pdf":
            content_type = "application/pdf"
        elif file_extension in ["jpg", "jpeg", "png"]:
            content_type = "image/png"
        else:
            content_type = "application/octet-stream"
        resp['Content-Type'] = content_type
        if download:
            resp['Content-Length'] = os.path.getsize(complete_file_path)
            resp['Content-Disposition'] = 'attachment; filename="' + file_name + '"'
        return resp
    raise Http404


@api_view(['GET'])
def get_merchant_logo_by_id(request):
    merchant_id = request.query_params.get('merchant_id')
    download = request.query_params.get('download')
    logo_path = merchant_data_service.get_logo_path_by_id(merchant_id)
    if logo_path is None:
        raise Http404
    complete_file_path = os.getcwd() + "/" + logo_path
    if os.path.exists(complete_file_path):
        resp = StreamingHttpResponse(
            streaming_content=open(complete_file_path, 'rb'))
        file_name = "Logo_" + merchant_id + "." + logo_path.split(".")[-1]
        resp['Content-Type'] = 'image/png'
        if download:
            resp['Content-Length'] = os.path.getsize(complete_file_path)
            resp['Content-Disposition'] = 'attachment; filename="' + file_name + '"'
        return resp
    raise Http404
