from datetime import datetime
from apis.database_models.verification import Verification
from apis.database_models.merchant_data import merchant_data
from apis.enums.kyccodes import KycStatus
from apis.utils.custom_exceptions import UserNotVerifiedException, DataNotFoundException, DocumentsNotVerifiedException
from apis.database_service import login_service, merchant_data_service
from ..database_service.email_service import email_validation, email_merchant_validation
from ..configuration.config import Configuration
from apis.database_service import merchant_document_service
from apis.database_models.document_type_master import DocumentTypeMaster
from ..database_service import email_service
from apis.database_models.kyc_audit_trails import KYCAuditTrails
from apis.enums.merchant_document_status import MerchantDocumentStatus
from apis.utils import custom_exceptions
from apis.database_service import bank_name_service
from apis.utils import Validator
from apis.database_service.logger import logger
from apis.database_models.kyc_consent import kyc_consent


def get_by_login_id(login_id):
    try:
        return Verification.objects.get(login_id=login_id)
    except Verification.DoesNotExist:
        raise DataNotFoundException("No KYC data found for the login id")


def get_document_type(doc_type_id):
    return DocumentTypeMaster.objects.get(id=doc_type_id)


def approve_kyc(kyc_data: Verification, approved_by):
    verified = KycStatus.VERIFIED.value
    if (
            kyc_data.general_info_status != verified
            or kyc_data.merchant_info_status != verified
            or kyc_data.business_info_status != verified
            or kyc_data.settlement_info_status != verified
            or kyc_data.status != verified
    ):
        raise UserNotVerifiedException("Please verify all the KYC information")
    kyc_data.approved_by = login_service.get_login_master(approved_by)
    kyc_data.approved_date = datetime.now()
    kyc_data.is_approved = True
    kyc_data.status = KycStatus.APPROVED.value
    merchant = merchant_data_service.merchant_data_by_login_id(kyc_data.login_id.loginMasterId)
    merchant.status = KycStatus.APPROVED.value
    merchant.save()
    kyc_data.save()
    email_merchant_validation(kyc_data.login_id.email, "kyc-merchant", kyc_data.login_id.name,
                              kyc_data.login_id.username)
    return kyc_data


def verify_kyc(kyc_data: Verification):
    verified = KycStatus.VERIFIED.value
    approved = KycStatus.APPROVED.value
    if (kyc_data.general_info_status != verified or kyc_data.merchant_info_status != verified
            or kyc_data.business_info_status != verified or kyc_data.settlement_info_status != verified):
        raise UserNotVerifiedException("Please verify all the KYC information")
    merchant = merchant_data_service.validate_required_docs(kyc_data.login_id.loginMasterId)
    check_merchant_doc = merchant_document_service.get_merchant_document_by_login_id(kyc_data.login_id.loginMasterId)
    for doc_status in check_merchant_doc:
        if doc_status.status != verified and doc_status.status != approved:
            raise DocumentsNotVerifiedException("Please verify all documents")
    kyc_data.status = verified
    kyc_data.is_verified = True
    kyc_data.verified_date = datetime.now()
    merchant.status = verified
    merchant.save()
    kyc_data.save()
    email_validation(Configuration.get_Property("APPROVER_EMAIL"), "Approve",
                     Configuration.get_Property("APPROVER_NAME"),
                     kyc_data.login_id.name,
                     "Verified", "Approve", kyc_data.login_id.username,
                     kyc_data.login_id.mobileNumber)
    return {"message": "KYC verified successfully", "status": True}


def reject_kyc(kyc_data: Verification, comments, reject_by):
    rejected = KycStatus.REJECTED.value
    merchant = merchant_data_service.merchant_data_by_login_id(kyc_data.login_id.loginMasterId)
    kyc_data.status = kyc_data.merchant_info_status = kyc_data.business_info_status = kyc_data.general_info_status = kyc_data.settlement_info_status = rejected
    kyc_data.merchant_info_reject_comments = kyc_data.business_info_reject_comments = kyc_data.general_info_reject_comments = kyc_data.settlement_info_reject_comments = rejected
    check_merchant_doc = merchant_document_service.get_merchant_document_by_login_id(kyc_data.login_id.loginMasterId)
    for doc_status in check_merchant_doc:
        doc_status.status = MerchantDocumentStatus.REJECTED.value
        doc_status.isApproved = False
        doc_status.modifiedBy = reject_by
        doc_status.comment = rejected
        doc_status.save()
        logger(f"merchant document: {doc_status.documentId} is "
               f"rejected by {reject_by} of merchant {doc_status.merchant.merchantId}")
    kyc_data.comments = comments
    kyc_data.is_verified = False
    kyc_data.is_approved = False
    kyc_data.kyc_reject = datetime.now()
    merchant.status = rejected
    merchant.save()
    kyc_data.save()
    login_data = login_service.get_login_master(kyc_data.login_id.loginMasterId)
    email_service.email_kyc_reject_validation(login_data.email, "kyc-reject", login_data.name,
                                              "All KYC")
    return {"message": "KYC rejected successfully", "status": True}


def update_tab_status_by_field(login_id, field_name, field_value):
    try:
        Verification.objects.filter(login_id=login_id).update(
            **{field_name: field_value, "status": KycStatus.PENDING.value})
    except Exception as e:
        raise Exception(e.args)


def reverse_kyc_approver_to_verifier(kyc_data: Verification, comments, approved_by):
    Processing = KycStatus.PROCESSING.value
    Pending = KycStatus.PENDING.value
    kyc_data.status = kyc_data.merchant_info_status = kyc_data.business_info_status = kyc_data.general_info_status = kyc_data.settlement_info_status = Pending
    kyc_data.is_verified = False
    merchant = merchant_data_service.merchant_data_by_login_id(kyc_data.login_id.loginMasterId)
    merchant.status = Processing
    check_merchant_doc = merchant_document_service.get_merchant_document_by_login_id(kyc_data.login_id.loginMasterId)
    # for get_doc_status in check_merchant_doc:
    #     get_doc_status.status = Pending
    #     get_doc_status.comment = "Verification Pending"
    #     get_doc_status.save()
    # kyc_data.save()
    # merchant.save()
    # kyc_audit_save_reverse_info(kyc_data.login_id.loginMasterId, approved_by, comments)
    return {"message": "KYC Reversed to Verifier", "status": True}


def re_approval(kyc_data: Verification, comments, approved_by):
    Verified = KycStatus.VERIFIED.value
    kyc_data.status = kyc_data.merchant_info_status = kyc_data.business_info_status = kyc_data.general_info_status = kyc_data.settlement_info_status = Verified
    kyc_data.is_approved = False
    merchant = merchant_data_service.merchant_data_by_login_id(kyc_data.login_id.loginMasterId)
    merchant.status = Verified
    check_merchant_doc = merchant_document_service.get_merchant_document_by_login_id(kyc_data.login_id.loginMasterId)
    # for get_doc_status in check_merchant_doc:
    #     get_doc_status.status = Verified
    #     get_doc_status.comment = "Approval Pending"
    #     get_doc_status.isApproved = False
    #     get_doc_status.save()
    # kyc_data.save()
    # merchant.save()
    # kyc_audit_save_reverse_info(kyc_data.login_id.loginMasterId, approved_by, comments)
    return {"message": "KYC Reversed to Re-Approval", "status": True}


def re_submit(kyc_data: Verification, comments, approved_by):
    Verified = KycStatus.VERIFIED.value
    kyc_data.status = kyc_data.merchant_info_status = kyc_data.business_info_status = \
        kyc_data.general_info_status = kyc_data.settlement_info_status = KycStatus.NOT_FILLED.value
    kyc_data.is_approved = False
    merchant = merchant_data_service.merchant_data_by_login_id(kyc_data.login_id.loginMasterId)
    # merchant.status = KycStatus.PENDING.value
    # kyc_data.save()
    # merchant.save()
    # kyc_audit_save_reverse_info(kyc_data.login_id.loginMasterId, approved_by, comments)
    return {"message": "KYC Reversed to Re-Submit", "status": True}


def kyc_audit_save_reverse_info(merchant_login_id, login_id, remarks):
    kyc_audit = KYCAuditTrails()
    kyc_audit.merchant_login_id = login_service.get_login_master(merchant_login_id)
    kyc_audit.login_id = login_service.get_login_master(login_id)
    kyc_audit.remarks = remarks
    kyc_audit.save()


def save_refer_zone_data(Merchant_data: merchant_data, approver_id, sourcing_point, sourcing_code):
    Merchant_data.sourcing_point = sourcing_point
    Merchant_data.sourcing_code = sourcing_code
    Merchant_data.refer_by = login_service.get_login_master(approver_id)
    Merchant_data.modifiedDate = datetime.now()
    Merchant_data.save()
    return {"message": "Data Updated", "status": True}


def update_kyc_consent_false(login_id):
    kyc_consent_update = None
    try:
        kyc_consent_update = get_kyc_consent_info(login_id)
    except Exception:
        kyc_consent_update = kyc_consent()
    kyc_consent_update.updated_on = datetime.now()
    kyc_consent_update.term_condition = False
    kyc_consent_update.save()
    return {"message": "Data Updated", "status": True}


def get_kyc_consent_info(login_id):
    try:
        return kyc_consent.objects.get(login_id=login_id)
    except Exception:
        raise DataNotFoundException("No KYC data found for the login id")
