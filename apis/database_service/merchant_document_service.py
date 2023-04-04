import traceback
from datetime import datetime

from django.core.files.storage import default_storage
from django.db import transaction

from apis.configuration.config import Configuration
from apis.database_models.business_doc_type_mapper import business_doc_type_mapper
from apis.database_models.merchant_data import merchant_data
from apis.database_models.merchant_document import merchant_document
from apis.database_models.document_type_master import DocumentTypeMaster
from apis.database_service import merchant_data_service, verification_service
from apis.enums.kyccodes import KycStatus
from apis.enums.merchant_document_status import MerchantDocumentStatus
from apis.enums.merchantstatus import MerchantStatusCode
from apis.utils.aws_bucket import S3BucketService
from apis.utils.custom_exceptions import DocumentNotApprovedException, DocumentNotVerifiedException, \
    DataNotFoundException, KycNotFilledException
from ..database_service import email_service
from ..database_service import login_service
from apis.database_service.logger import logger


@transaction.atomic
def save_merchant_document(merchant_document_data):
    try:
        validation_response = validate_kyc_doc(merchant_document_data['files'])
        if not validation_response['status']:
            return validation_response
        # current_path = os.getcwd()
        doc_folder = Configuration.get_Property('MERCHANT_DOC_FOLDER')
        login_id = merchant_document_data['login_id']
        merchant = merchant_data_service.merchant_data_by_login_id(login_id)
        merchant_doc = merchant_document()
        merchant_doc.merchant = merchant
        merchant_doc.modifiedBy = login_id
        file_path = doc_folder + "/MERCHANT_" + str(merchant.merchantId)
        file_name = generate_kyc_doc_name(merchant_document_data['files'])
        merchant_doc.name = file_name
        merchant_doc.type = merchant_document_data['type']
        merchant_doc.isLatest = True
        merchant_doc.createdBy = login_id
        merchant_doc.status = MerchantDocumentStatus.PENDING.value
        old_document = get_document_by_merchant_id_and_type_id(merchant.merchantId, merchant_document_data['type'].id)
        if old_document.exists():
            old_document.update(isLatest=False)
        # for saving on local filesystem
        # complete_file_path = current_path + "/" + file_path
        # save_file(merchant_document_data['files'], complete_file_path)
        # for saving on aws s3 bucket
        bucket = S3BucketService()
        file_url = bucket.upload_file(merchant_document_data['files'], file_path, file_name)
        merchant_doc.filePath = file_url
        merchant_doc.save()
        logger(f"Merchant {file_name} save successfully of path {file_path}")
        return {"message": "Merchant document saved successfully", "status": True}
    except Exception as e:
        transaction.set_rollback(True)
        raise Exception(e)


def validate_kyc_doc(file):
    file_extension = file.name.split('.')[-1].lower()
    print(">>>>>>>>>>>", file_extension)
    allowed_types = Configuration.get_Property("ALLOWED_FILE_TYPES")
    if file_extension not in allowed_types:
        return {'status': False, 'message': 'File type not allowed. Allowed file types are: ' + allowed_types}
    file_size = file.size / (1024 * 1024)
    max_file_size = Configuration.get_Property("MAX_FILE_SIZE")
    if file_size > int(max_file_size):
        logger(f"File size exceeds maximum limit of  {max_file_size} MB")
        return {'status': False, 'message': 'File size exceeds maximum limit of ' + max_file_size + 'MB'}
    return {'status': True, 'message': 'File validated successfully'}


def save_file(file, file_path):
    file_name = default_storage.save(file_path, content=file)
    return file_name


def generate_kyc_doc_name(file):
    file_extension = file.name.split('.')[-1]
    file_name = file.name.replace('.' + file_extension, '')
    file_name = file_name.replace(' ', '_') + '_' + str(datetime.now().strftime("%Y%m%d%H%M%S")) + '.' + file_extension
    return file_name


def get_document_by_merchant_id_and_type_id(merchant_id, type_id):
    merchant_doc = merchant_document.objects.filter(merchant=merchant_id, type=type_id)
    return merchant_doc


def get_document_path_by_id(document_id):
    try:
        file_path = merchant_document.objects.only('filePath').get(documentId=document_id)
        return file_path
    except Exception:
        traceback.print_exc()
        return None


@transaction.atomic
def save_single_merchant_document(merchant_document_data):
    try:
        validation_response = validate_kyc_doc(merchant_document_data['files'])
        if not validation_response['status']:
            return validation_response
        doc_folder = Configuration.get_Property('MERCHANT_DOC_FOLDER')
        login_id = merchant_document_data['login_id']
        merchant = merchant_data_service.merchant_data_by_login_id(login_id)
        merchant_doc = merchant_document()
        merchant_doc.merchant = merchant
        merchant_doc.modifiedBy = login_id
        file_path = doc_folder + "/SINGLE_FILE/MERCHANT_" + str(merchant.merchantId)
        file_name = generate_kyc_doc_name(merchant_document_data['files'])
        merchant_doc.name = file_name
        merchant_doc.filePath = file_path + "/" + file_name
        merchant_doc.type = merchant_document_data['type']
        merchant_doc.isLatest = True
        merchant_doc.createdBy = login_id
        merchant_doc.status = MerchantDocumentStatus.PENDING.value
        old_document = get_document_by_merchant_id_and_type_id(merchant.merchantId, merchant_document_data['type'].id)
        if old_document.exists():
            old_document.update(isLatest=False)
        # current_path = os.getcwd()
        # complete_file_path = current_path + "/" + merchant_doc.filePath
        # save_file(merchant_document_data['files'], complete_file_path)
        bucket = S3BucketService()
        file_url = bucket.upload_file(merchant_document_data['files'], file_path, file_name)
        merchant_doc.filePath = file_url
        merchant_doc.save()
        merchant_data_service.update_merchant_term_condition_status(login_id)
        logger(f"Merchant {file_name} save successfully of path {file_path} of merchant id {merchant.merchantId}")
        return {"message": "Merchant document saved successfully", "status": True}
    except Exception as e:
        transaction.set_rollback(True)
        raise Exception(e)


def doc_by_merchant_id(merchant_id):
    return merchant_document.objects.filter(merchant=merchant_id, isLatest=True)


def verify_document_status(merchant_id):
    merchant_docs = doc_by_merchant_id(merchant_id)
    if merchant_docs.filter(isApproved=False).exists():
        logger(f"Merchant document is not approved against merchant id {merchant_id}")
        raise DocumentNotApprovedException("Please approve the documents before proceeding")


def get_document_by_id(document_id):
    try:
        return merchant_document.objects.get(documentId=document_id)
    except Exception:
        raise DataNotFoundException("Document not found for the given document id")


def approve_merchant_document(document_id, approved_by):
    merchant_doc = get_document_by_id(document_id)
    if merchant_doc.status == MerchantDocumentStatus.VERIFIED.value:
        merchant_doc.status = MerchantDocumentStatus.APPROVED.value
        merchant_doc.isApproved = True
        merchant_doc.approvedBy = approved_by
        merchant_doc.modifiedBy = approved_by
        merchant_doc.comment = "Document Approved"
        merchant_doc.approvedDate = datetime.now()
        merchant_doc.save()
        return {"message": "Merchant document approved successfully", "status": True}
    else:
        raise DocumentNotVerifiedException("Please verify the documents before approving")


def verify_merchant_document(document_id, verified_by):
    merchant_doc = get_document_by_id(document_id)
    merchant_doc.status = MerchantDocumentStatus.VERIFIED.value
    merchant_doc.modifiedBy = verified_by
    merchant_doc.comment = "Document Verified"
    merchant_doc.save()
    return {"message": "Merchant document verified successfully", "status": True}


def reject_merchant_document(document_id, rejected_by, comment):
    merchant_doc = get_document_by_id(document_id)
    merchant_doc.status = MerchantDocumentStatus.REJECTED.value
    merchant_doc.isApproved = False
    merchant_doc.modifiedBy = rejected_by
    merchant_doc.comment = comment
    merchant_doc.modifiedDate = datetime.now()
    merchant: merchant_data = merchant_doc.merchant
    merchant.status = MerchantStatusCode.PROCESSING.value
    verification = verification_service.get_by_login_id(merchant.loginMasterId)
    login_data = login_service.get_login_master(merchant.loginMasterId)
    kyc_consent_date = verification_service.get_kyc_consent_info(merchant.loginMasterId)
    document: DocumentTypeMaster = merchant_doc.type
    verification.status = KycStatus.PROCESSING.value
    verification.is_approved = False
    verification.is_verified = False
    kyc_consent_date.term_condition = False
    kyc_consent_date.updated_on = datetime.now()
    kyc_consent_date.save()
    verification.save()
    merchant.save()
    merchant_doc.save()
    email_service.email_kyc_reject_validation(login_data.email, "kyc-reject", login_data.name, document.name)
    return {"message": "Merchant document rejected successfully", "status": True}


def get_merchant_document_by_login_id(login_id):
    merchant = merchant_data_service.merchant_data_by_login_id(login_id)
    return doc_by_merchant_id(merchant.merchantId)


@transaction.atomic
def save_merchant_aadhar(merchant_document_data):
    try:
        validation_response = validate_kyc_doc(merchant_document_data['files'])
        if not validation_response['status']:
            return validation_response
        doc_folder = Configuration.get_Property('MERCHANT_DOC_FOLDER')
        file = merchant_document_data['files']
        login_id = merchant_document_data['login_id']
        merchant = merchant_data_service.merchant_data_by_login_id(login_id)
        merchant_doc = merchant_document()
        merchant_doc.merchant = merchant
        merchant_doc.modifiedBy = login_id
        file_path = doc_folder + "/MERCHANT_" + str(merchant.merchantId)
        if merchant_document_data['file_number'] == 0:
            file.name = "aadhaar front" + "." + str(file.name.split(".")[-1])
        elif merchant_document_data['file_number'] == 1:
            file.name = "aadhaar back" + "." + str(file.name.split(".")[-1])
        print("file name: ", file.name)
        merchant_doc.name = file.name
        file_name = generate_kyc_doc_name(file)
        merchant_doc.type = merchant_document_data['type']
        merchant_doc.isLatest = True
        merchant_doc.createdBy = login_id
        merchant_doc.status = MerchantDocumentStatus.PENDING.value
        # current_path = os.getcwd()
        # complete_file_path = current_path + "/" + merchant_doc.filePath
        # save_file(merchant_document_data['files'], complete_file_path)
        bucket = S3BucketService()
        file_url = bucket.upload_file(file, file_path, file_name)
        merchant_doc.filePath = file_url
        merchant_doc.save()
        merchant_data_service.update_merchant_term_condition_status(login_id)
        logger(f"Merchant {file_name} save successfully of file path {file_path} of merchant id {merchant.merchantId}")
        return merchant_doc
    except Exception as e:
        transaction.set_rollback(True)
        raise Exception(e)


def remove_merchant_document(document_id, removed_by):
    merchant_doc = get_document_by_id(document_id)
    if merchant_doc.status == MerchantDocumentStatus.VERIFIED.value or \
            merchant_doc.status == MerchantDocumentStatus.APPROVED.value:
        logger(f"Merchant doc is not deleted because: {merchant_doc.status}")
        return {"message": merchant_doc.status + " documents cannot be deleted", "status": False}
    merchant_doc.status = MerchantDocumentStatus.REJECTED.value
    merchant_doc.modifiedBy = removed_by
    merchant_doc.comment = "Document removed by " + str(removed_by)
    merchant_doc.status = MerchantDocumentStatus.REMOVED.value
    merchant_doc.isLatest = False
    merchant_doc.save()
    logger(f"Merchant doc removed successfully")
    return {"message": "Merchant document removed successfully", "status": True}


def doc_status_by_login_id(login_id):
    merchant_docs = get_merchant_document_by_login_id(login_id)
    not_submitted = MerchantDocumentStatus.NOT_SUBMITTED.value
    submitted = MerchantDocumentStatus.SUBMITTED.value
    pending = MerchantDocumentStatus.PENDING.value
    verified = MerchantDocumentStatus.VERIFIED.value
    approved = MerchantDocumentStatus.APPROVED.value
    rejected = MerchantDocumentStatus.REJECTED.value
    if not merchant_docs:
        return not_submitted
    if rejected in [doc.status for doc in merchant_docs]:
        return rejected
    if pending in [doc.status for doc in merchant_docs]:
        return pending
    if verified in [doc.status for doc in merchant_docs]:
        return verified
    return approved


def get_required_docs(business_type_id):
    business_type_docs = business_doc_type_mapper.objects.filter(business_type_id=business_type_id, is_required=True)
    doc_ids = [int(btd.doc_type_id) for btd in business_type_docs]
    return doc_ids
