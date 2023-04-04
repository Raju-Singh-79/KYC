import os
from datetime import datetime
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, action
from rest_framework.response import Response

from apis.utils import Validator
from apis.utils import custom_exceptions
from ..database_models.verification import Verification
from ..database_service import (merchant_data_service, verification_service, role_service, merchant_document_service, )
from ..enums.kyccodes import KycStatus
from ..enums.rolecodes import Role
from ..serializers.verification_serializer import VerificationSerializer
from ..utils.PaginationMeta import PaginationMeta
from ..database_service import email_service
from ..database_service import login_service
from apis.database_service.logger import logger


@api_view(["PUT"])
def save_general_info_api(request):
    data = request.data
    name = data.get("name")
    contact_number = data.get("contact_number")
    email_id = data.get("email_id")
    login_id = data.get("login_id")
    aadhar_number = data.get("aadhar_number")
    modified_by = data.get("modified_by")
    contact_designation = data.get("contact_designation")

    request_fields = ["name", "contact_number", "email_id", "login_id", "modified_by", "aadhar_number", ]

    Validator.validate_request_data(request_fields, data)
    save_general_info_response = merchant_data_service.save_general_info(login_id, name, contact_number, email_id,
                                                                         aadhar_number, modified_by,
                                                                         contact_designation)

    return Response(save_general_info_response, status=status.HTTP_200_OK if save_general_info_response["status"]
    else status.HTTP_400_BAD_REQUEST, )


@api_view(["POST"])
def save_merchant_info_api(request):
    data = request.data
    company_name = data.get("company_name")
    registerd_with_gst = data.get("registerd_with_gst")
    gst_number = data.get("gst_number")
    pan_card = data.get("pan_card")
    signatory_pan = data.get("signatory_pan")
    name_on_pancard = data.get("name_on_pancard")
    pin_code = data.get("pin_code")
    city_id = data.get("city_id")
    state_id = data.get("state_id")
    registered_business_address = data.get("registered_business_address")
    operational_address = data.get("operational_address")
    login_id = data.get("login_id")
    logo = request.FILES.get("files")
    modified_by = data.get("modified_by")
    request_fields = ["company_name", "registerd_with_gst", "pan_card", "signatory_pan", "name_on_pancard",
                      "pin_code", "city_id", "state_id", "operational_address",
                      "login_id", "modified_by", ]

    Validator.validate_request_data(request_fields, data)
    if registerd_with_gst == "True" and not gst_number:
        return Response(
            {
                "message": "Please provide gst_number or make registered with gst false",
                "response_code": 400,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    if logo:
        Validator.validate_file(logo)
        save_file_response = merchant_data_service.save_merchant_logo(logo, login_id)
        if not save_file_response["status"]:
            return Response(save_file_response, status=status.HTTP_400_BAD_REQUEST)
        logo_path = save_file_response["file_path"]
    else:
        logo_path = None

    merchant_data_service.save_merchant_address(login_id, operational_address, city_id, state_id, pin_code, modified_by)

    save_merchant_info_response = merchant_data_service.save_merchant_info(company_name, logo_path, registerd_with_gst,
                                                                           gst_number, pan_card, signatory_pan,
                                                                           name_on_pancard, pin_code, city_id, state_id,
                                                                           registered_business_address,
                                                                           operational_address, login_id, modified_by)

    if save_merchant_info_response:
        return Response(save_merchant_info_response, status=status.HTTP_200_OK if save_merchant_info_response["status"]
        else status.HTTP_400_BAD_REQUEST, )


@api_view(["PUT"])
def save_business_info_api(request):
    data = request.data
    business_type = data.get("business_type")
    business_category = data.get("business_category")
    business_model = data.get("business_model")
    billing_label = data.get("billing_label")
    company_website = data.get("company_website")
    erp_check = data.get("erp_check")
    platform_id = data.get("platform_id")
    collection_type_id = data.get("collection_type_id")
    collection_frequency_id = data.get("collection_frequency_id")
    expected_transactions = data.get("expected_transactions")
    form_build = data.get("form_build")
    ticket_size = data.get("ticket_size")
    login_id = data.get("login_id")
    modified_by = data.get("modified_by")
    avg_ticket_size = data.get("avg_ticket_size")
    website_app_url = data.get("website_app_url")
    is_website_url = data.get("is_website_url")

    request_fields = ["company_website", "erp_check", "platform_id", "collection_type_id", "collection_frequency_id",
                      "expected_transactions", "form_build", "ticket_size", "login_id", "modified_by", "is_website_url",
                      "avg_ticket_size", ]

    Validator.validate_request_data(request_fields, data)

    if is_website_url == "True" and not website_app_url:
        return Response(
            {
                "message": "Please provide website_url or make website_url false",
                "response_code": 400,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    business_info_response = merchant_data_service.save_business_info(business_type, business_category,
                                                                      business_model,
                                                                      billing_label, company_website, erp_check,
                                                                      platform_id, collection_type_id,
                                                                      collection_frequency_id,
                                                                      expected_transactions,
                                                                      form_build, ticket_size, login_id,
                                                                      modified_by,
                                                                      website_app_url, is_website_url,
                                                                      avg_ticket_size)

    if business_info_response:
        return Response(business_info_response, status=status.HTTP_200_OK if business_info_response["status"]
        else status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
def save_settlement_info_api(request):
    data = request.data
    account_holder_name = data.get("account_holder_name")
    account_number = data.get("account_number")
    ifsc_code = data.get("ifsc_code")
    bank_id = data.get("bank_id")
    account_type = data.get("account_type")
    branch = data.get("branch")
    login_id = data.get("login_id")
    modified_by = data.get("modified_by")

    request_fields = ["account_holder_name", "account_number", "ifsc_code", "bank_id", "account_type", "branch",
                      "login_id", "modified_by", ]

    Validator.validate_request_data(request_fields, data)

    settlement_info_response = merchant_data_service.save_settlement_info_other(account_holder_name, account_number,
                                                                                ifsc_code, bank_id, account_type,
                                                                                branch, login_id, modified_by, )

    return Response(settlement_info_response, status=status.HTTP_200_OK if settlement_info_response["status"]
    else status.HTTP_400_BAD_REQUEST,
                    )


class VerificationApi(viewsets.ViewSet):
    query_set = Verification.objects.all()

    def list(self, request):
        order_by = request.query_params.get("order_by", "id")
        queryset = Verification.objects.all().order_by(order_by)
        paginator = PaginationMeta()
        page = paginator.paginate_queryset(queryset, request)
        if page is not None:
            serializer = VerificationSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        else:
            serializer = VerificationSerializer(queryset, many=True)
            return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = get_object_or_404(self.query_set, login_id=pk)
        serializer = VerificationSerializer(queryset)
        response = serializer.data
        document_status = merchant_document_service.doc_status_by_login_id(login_id=pk)
        response["document_status"] = document_status
        return Response(response)

    @action(detail=False, methods=["post"], url_path="update")
    def kyc_update(self, request):
        data = request.data
        allowed_roles = [Role.VERIFIER.value, Role.APPROVER.value]
        verified_by = [data[key] for key in data if "verified_by" in key][0]
        verifier_role = role_service.get_role_by_login_id(verified_by)
        check_access_response = role_service.check_role_access(verifier_role, allowed_roles)
        if not check_access_response:
            raise custom_exceptions.UnauthorizedException("You are not authorized to perform this action")
        login_id = request.data.get("login_id")
        verification_data = verification_service.get_by_login_id(login_id)
        serializer = VerificationSerializer(verification_data, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger(f"Kyc verified successfully of : {request.data}")
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"], url_path="tab-reject")
    def kyc_tab_reject(self, request):
        data = request.data
        allowed_roles = [Role.VERIFIER.value, Role.APPROVER.value]
        rejected_by = [data[key] for key in data if "rejected_by" in key]
        if len(rejected_by) < 1 or not data.get("login_id"):
            raise custom_exceptions.IncompleteDataException("Please provide both login_id and rejected_by")
        rejected_by = rejected_by[0]
        rejecter_role = role_service.get_role_by_login_id(rejected_by)
        check_access_response = role_service.check_role_access(rejecter_role, allowed_roles)
        if not check_access_response:
            raise custom_exceptions.UnauthorizedException("You are not authorized to perform this action")
        login_id = request.data.get("login_id")
        verification_data: Verification = verification_service.get_by_login_id(login_id)
        login_data = login_service.get_login_master(login_id)
        if data.get("general_info_rejected_by") and data.get("general_info_reject_comments"):
            verification_data.general_info_status = KycStatus.REJECTED.value
            verification_data.general_info_reject_date = datetime.now()
            verification_data.general_info_reject_comments = data.get("general_info_reject_comments")
            email_service.email_kyc_reject_validation(login_data.email, "kyc-reject", login_data.name, "Contact Info")
            logger(f"Merchant Contact Info reject by {rejected_by}")
        elif data.get("merchant_info_rejected_by") and data.get("merchant_info_reject_comments"):
            verification_data.merchant_info_status = KycStatus.REJECTED.value
            verification_data.merchant_info_reject_date = datetime.now()
            verification_data.merchant_info_reject_comments = data.get("merchant_info_reject_comments")
            email_service.email_kyc_reject_validation(login_data.email, "kyc-reject", login_data.name,
                                                      "Business Details")
            logger(f"Business overview data is reject by {rejected_by}")
        elif data.get("business_info_rejected_by") and data.get("business_info_reject_comments"):
            verification_data.business_info_status = KycStatus.REJECTED.value
            verification_data.business_info_reject_date = datetime.now()
            verification_data.business_info_reject_comments = data.get("business_info_reject_comments")
            email_service.email_kyc_reject_validation(login_data.email, "kyc-reject", login_data.name,
                                                      "Business Overview")
            logger(f"Business details data is reject by {rejected_by}")
        elif data.get("settlement_info_rejected_by") and data.get("settlement_info_reject_comments"):
            verification_data.settlement_info_status = KycStatus.REJECTED.value
            verification_data.settlement_info_reject_date = datetime.now()
            email_service.email_kyc_reject_validation(login_data.email, "kyc-reject", login_data.name, "Bank Details")
            verification_data.settlement_info_reject_comments = data.get("settlement_info_reject_comments")
            logger(f"Bank details data is reject by {rejected_by}")
        else:
            logger(f"comments or reject by is required")
            raise custom_exceptions.IncompleteDataException("Reject comments is required")
        verification_service.update_kyc_consent_false(login_id)
        verification_data.save()
        return Response(VerificationSerializer(verification_data).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path="verify")
    def kyc_verify(self, request):
        login_id = request.data.get("login_id")
        verified_by = request.data.get("verified_by")
        if not login_id or not verified_by:
            raise custom_exceptions.IncompleteDataException("Please provide login_id and verified_by")
        allowed_roles = [Role.VERIFIER.value, Role.APPROVER.value]
        verifier_role = role_service.get_role_by_login_id(verified_by)
        check_access_response = role_service.check_role_access(verifier_role, allowed_roles)
        if not check_access_response:
            raise custom_exceptions.UnauthorizedException("You are not authorized to perform this action")
        verification_data = verification_service.get_by_login_id(login_id)
        verification_service.verify_kyc(verification_data)
        logger(f"KYC verified successfully by: {verified_by} of merchant: {login_id}")
        return Response({"message": "KYC verified successfully", "status_code": 200}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path="reject")
    def kyc_reject(self, request):
        login_id = request.data.get("login_id")
        rejected_by = request.data.get("rejected_by")
        comments = request.data.get("comments")
        request_fields = ["login_id", "rejected_by", "comments"]
        Validator.validate_request_data(request_fields, request.data)
        allowed_roles = [Role.VERIFIER.value, Role.APPROVER.value]
        rejecter_role = role_service.get_role_by_login_id(rejected_by)
        check_access_response = role_service.check_role_access(rejecter_role, allowed_roles)
        if not check_access_response:
            raise custom_exceptions.UnauthorizedException("You are not authorized to perform this action")
        verification_data = verification_service.get_by_login_id(login_id)
        verification_service.reject_kyc(verification_data, comments, rejected_by)
        verification_service.update_kyc_consent_false(login_id)
        logger(f"All kyc data is rejected by: {rejected_by} of merchant {login_id}")
        return Response({"message": "KYC rejected successfully", "status_code": 200}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path="approve")
    def kyc_approve(self, request):
        data = request.data
        login_id = data.get("login_id")
        approved_by = data.get("approved_by")
        if not login_id or not approved_by:
            raise custom_exceptions.IncompleteDataException("Please provide login id and approved by")
        allowed_roles = [Role.APPROVER.value]
        approver_role = role_service.get_role_by_login_id(approved_by)
        check_access_response = role_service.check_role_access(approver_role, allowed_roles)
        if not check_access_response:
            raise custom_exceptions.UnauthorizedException("You are not authorized to perform this action")
        verification_data = verification_service.get_by_login_id(login_id)
        merchant_id = merchant_data_service.merchant_data_by_login_id(login_id).merchantId
        merchant_document_service.verify_document_status(merchant_id)
        verification_service.approve_kyc(verification_data, approved_by)
        logger(f"Kyc Approved successfully by: {approved_by} of merchant: {login_id}")
        return Response({"message": "KYC approved successfully", "status_code": 200}, status=status.HTTP_200_OK)


@api_view(["POST"])
def kyc_consent_api(request):
    data = request.data
    login_id = data.get("login_id")
    term_condition = data.get("term_condition")
    submitted_by = data.get("submitted_by")
    request_fields = ["login_id", "term_condition", "submitted_by"]
    try:
        Validator.validate_request_data(request_fields, data)
    except Exception:
        raise custom_exceptions.IncompleteDataException("Please Accept Term & Condition")
    kyc_consent_response = merchant_data_service.kyc_submit(login_id, term_condition, submitted_by)

    if kyc_consent_response:
        return Response(kyc_consent_response, status=status.HTTP_200_OK if kyc_consent_response["status"]
        else status.HTTP_400_BAD_REQUEST, )


@api_view(["POST"])
def test(request):
    from apis.utils.custom_storage import MediaStorage

    file_obj = request.FILES.get("file", "")
    file_directory_within_bucket = "cobDocs/MERCHANT_01"
    file_path_within_bucket = os.path.join(file_directory_within_bucket, file_obj.name)
    media_storage = MediaStorage()
    media_storage.save(file_path_within_bucket, file_obj)
    file_url = media_storage.url(file_path_within_bucket)
    return file_url


class ReverseKYC(viewsets.ViewSet):
    query_set = Verification.objects.all()

    @action(detail=False, methods=["post"], url_path="approver-to-verifier")
    def approver_to_verifier(self, request):
        data = request.data
        login_id = data.get("login_id")
        approved_by = data.get("approved_by")
        comments = data.get("comments")
        request_fields = ["login_id", "approved_by", "comments"]
        Validator.validate_request_data(request_fields, data)
        allowed_roles = [Role.APPROVER.value]
        approver_role = role_service.get_role_by_login_id(approved_by)
        check_access_response = role_service.check_role_access(approver_role, allowed_roles)
        if not check_access_response:
            raise custom_exceptions.UnauthorizedException("You are not authorized to perform this action")
        verification_data = verification_service.get_by_login_id(login_id)
        verification_service.reverse_kyc_approver_to_verifier(verification_data, comments, approved_by)
        return Response({"message": "KYC Reversed to Verifier", "status_code": 200}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path="re-approval")
    def re_approval(self, request):
        data = request.data
        login_id = data.get("login_id")
        approved_by = data.get("approved_by")
        comments = data.get("comments")
        request_fields = ["login_id", "approved_by", "comments"]
        Validator.validate_request_data(request_fields, data)
        allowed_roles = [Role.APPROVER.value]
        approver_role = role_service.get_role_by_login_id(approved_by)
        check_access_response = role_service.check_role_access(approver_role, allowed_roles)
        if not check_access_response:
            raise custom_exceptions.UnauthorizedException("You are not authorized to perform this action")
        verification_data = verification_service.get_by_login_id(login_id)
        verification_service.re_approval(verification_data, comments, approved_by)
        return Response({"message": "KYC Reversed to Re-Approved", "status_code": 200}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path="re-kyc-submit")
    def re_kyc_submit(self, request):
        data = request.data
        login_id = data.get("login_id")
        approved_by = data.get("approved_by")
        comments = data.get("comments")
        request_fields = ["login_id", "approved_by", "comments"]
        Validator.validate_request_data(request_fields, data)
        allowed_roles = [Role.APPROVER.value]
        approver_role = role_service.get_role_by_login_id(approved_by)
        check_access_response = role_service.check_role_access(approver_role, allowed_roles)
        if not check_access_response:
            raise custom_exceptions.UnauthorizedException("You are not authorized to perform this action")
        verification_data = verification_service.get_by_login_id(login_id)
        verification_service.re_submit(verification_data, comments, approved_by)
        return Response({"message": "KYC Reversed to Re-Submit", "status_code": 200}, status=status.HTTP_200_OK)


class ReferZone(viewsets.ViewSet):
    @action(detail=False, methods=["post"], url_path="save-refer-zone")
    def save_refer_zone(self, req):
        data = req.data
        approver_id = data.get("approver_id")
        login_id = data.get("login_id")
        sourcing_point = data.get("sourcing_point")
        sourcing_name = data.get("sourcing_code")
        request_fields = ["login_id", "approver_id", "sourcing_point", "sourcing_code"]
        Validator.validate_request_data(request_fields, data)
        allowed_roles = [Role.APPROVER.value]
        approver_role = role_service.get_role_by_login_id(approver_id)
        check_access_response = role_service.check_role_access(approver_role, allowed_roles)
        if not check_access_response:
            raise custom_exceptions.UnauthorizedException("You are not authorized to perform this action")
        merchant_data = merchant_data_service.merchant_data_by_login_id(login_id)
        verification_service.save_refer_zone_data(merchant_data, approver_id, sourcing_point, sourcing_name)
        logger(f"{approver_id} is referred to {login_id} for sourcing point{sourcing_point} and {sourcing_name}")
        return Response({"message": "Merchant Refer Zone Updated", "status_code": 200}, status=status.HTTP_200_OK)
