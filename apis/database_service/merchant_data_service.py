import os
import traceback

from apis.database_models.client_account_details import client_account_details
from apis.database_models.login_master import login_master
from apis.database_models.merchant_address import merchant_address
from apis.database_models.merchant_data import merchant_data
from apis.database_service import login_service, verification_service
from apis.database_service import merchant_document_service
from apis.database_service import otp_service
from apis.serializers.merchant_serializer import merchant_data_serializer
from apis.utils.custom_exceptions import (DataNotFoundException, MobileNumberNotVerifiedException,
                                          MailNotVerifiedException, UserAlreadyExistException, KycNotFilledException,
                                          KycFilledException)
from .verification_service import update_tab_status_by_field
from ..configuration.config import Configuration
from ..database_models.bank_master import bank_master
from ..database_models.kyc_consent import kyc_consent
from ..database_models.lookup_state import lookup_state
from ..database_models.verification import Verification
from ..enums.kyccodes import KycStatus
from ..enums.merchant_document_status import MerchantDocumentStatus
from ..enums.merchantstatus import MerchantStatusCode
from ..utils import custom_exceptions
from django.db.models import Q
from ..database_service.email_service import email_validation
from datetime import datetime
from apis.database_service.logger import logger


def validate_phone_and_mail(contact_number, email_id, login_id):
    try:
        by_mail = login_service.get_by_email(email_id)
        if by_mail.loginMasterId != login_id:
            raise UserAlreadyExistException("Email already registered")
    except DataNotFoundException:
        traceback.print_exc()
    try:
        by_mobile = login_service.get_by_mobile(contact_number)
        if by_mobile.loginMasterId != int(login_id):
            raise UserAlreadyExistException("Mobile number already registered")
    except DataNotFoundException:
        traceback.print_exc()
    validate_phone(contact_number)
    # validate_mail(email_id)


def validate_phone(contact_number):
    otp = otp_service.otp_by_phone(contact_number)
    if otp is None:
        raise MobileNumberNotVerifiedException("Please verify mobile number")


def validate_mail(email_id):
    otp = otp_service.otp_by_email(email_id)
    if otp is None:
        raise MailNotVerifiedException("Please verify email id")


def save_general_info(login_id, name, contact_number, email_id, aadhar_number, modified_by, contact_designation):
    check_kyc_status(login_id)
    update_merchant_term_condition_status(login_id)
    validate_phone_and_mail(contact_number, email_id, login_id)
    try:
        merchant = merchant_data_by_login_id(login_id)
    except Exception:
        traceback.print_exc()
        merchant = merchant_data()
    merchant.loginMasterId = login_id
    merchant.name = name
    merchant.aadharNumber = aadhar_number
    merchant.contactNumber = contact_number
    merchant.emailId = email_id
    merchant.contactDesignation = contact_designation
    merchant.modified_by = modified_by
    merchant.modifiedDate = datetime.now()
    merchant.isEmailVerified = True
    merchant.isContactNumberVerified = True
    merchant.status = MerchantStatusCode.PENDING.value
    merchant.save()
    login_master_data = login_master.objects.get(loginMasterId=login_id)
    if login_master_data.name != name:
        login_master_data.name = name
    if login_master_data.email != email_id:
        login_master_data.email = email_id
    if login_master_data.mobileNumber != contact_number:
        login_master_data.mobileNumber = contact_number
    login_master_data.save()
    logger(f"merchant data save successfully for login id: {login_id}")
    update_tab_status_by_field(login_id, "general_info_status", KycStatus.PENDING.value)
    return {"status": True, "message": "Merchant data saved successfully"}


def save_merchant_info(company_name, logo_path, registerd_with_gst, gst_number, pan_card, signatory_pan,
                       name_on_pancard, pin_code, city_id, state_id, registered_business_address,
                       operational_address, login_id, modified_by, ):
    check_kyc_status(login_id)
    update_merchant_term_condition_status(login_id)
    try:
        merchant_info_data = merchant_data_by_login_id(login_id)
    except Exception:
        traceback.print_exc()
        raise DataNotFoundException("Merchant data not found for the given login id")
    merchant_info_data.panCard = pan_card
    merchant_info_data.modified_by = modified_by
    merchant_info_data.modifiedDate = datetime.now()
    merchant_info_data.nameOnPanCard = name_on_pancard
    merchant_info_data.companyName = company_name
    merchant_info_data.registeredBusinessAdress = registered_business_address
    merchant_info_data.stateId = state_id
    merchant_info_data.pinCode = pin_code
    merchant_info_data.registerdWithGST = registerd_with_gst
    merchant_info_data.gstNumber = gst_number
    merchant_info_data.signatoryPAN = signatory_pan
    merchant_info_data.cityId = city_id
    merchant_info_data.operationalAddress = operational_address
    merchant_info_data.companyLogoPath = logo_path
    merchant_info_data.status = MerchantStatusCode.PENDING.value
    merchant_info_data.save()
    logger(f"merchant data save successfully for login id: {login_id}")
    update_tab_status_by_field(login_id, "merchant_info_status", KycStatus.PENDING.value)
    return {"status": True, "message": "Merchant data saved successfully"}


def merchant_data_by_client_code(client_code):
    try:
        merch_all_data = merchant_data.objects.get(clientCode=client_code)
        merch_data = merchant_data_serializer(merch_all_data).data
        return merch_data
    except Exception:
        traceback.print_exc()
        return None


def merchant_data_by_login_id(login_id) -> merchant_data:
    try:
        print("Fetching merchant data by login id ", login_id)
        merch_data = merchant_data.objects.get(loginMasterId=login_id)
        return merch_data
    except Exception:
        traceback.print_exc()
        raise DataNotFoundException("Merchant data not found for the given login id")


def save_merchant_logo(logo, login_id):
    try:
        merchant = merchant_data.objects.get(loginMasterId=login_id)
        current_path = os.getcwd()
        doc_folder = Configuration.get_Property("MERCHANT_DOC_FOLDER")
        file_path = doc_folder + "/MERCHANT_" + str(merchant.merchantId)
        file_name = merchant_document_service.generate_kyc_doc_name(logo)
        file_path = file_path + "/LOGO_" + file_name
        complete_file_path = current_path + "/" + file_path
        merchant_document_service.save_file(logo, complete_file_path)
        return {"status": True, "file_path": file_path}
    except Exception:
        traceback.print_exc()
        raise DataNotFoundException("Merchant data not found for the given login id")


def save_business_info(business_type, business_category, business_model, billing_label,
                       company_website, erp_check, platform_id, collection_type_id, collection_frequency_id,
                       expected_transactions, form_build, ticket_size, login_id, modified_by, website_app_url,
                       is_website_url, avg_ticket_size):
    check_kyc_status(login_id)
    update_merchant_term_condition_status(login_id)
    try:
        get_merchant_data = merchant_data_by_login_id(login_id)
    except Exception:
        traceback.print_exc()
        raise DataNotFoundException("Merchant data not found for the given login id")
    get_merchant_data.businessType = business_type
    get_merchant_data.businessCategory = business_category
    get_merchant_data.businessModel = business_model
    get_merchant_data.billingLabel = billing_label
    get_merchant_data.companyWebsite = company_website
    get_merchant_data.erpCheck = erp_check
    get_merchant_data.modified_by = modified_by
    get_merchant_data.modifiedDate = datetime.now()
    get_merchant_data.platformId = platform_id
    get_merchant_data.collectionTypeId = collection_type_id
    get_merchant_data.collectionFrequencyId = collection_frequency_id
    get_merchant_data.expectedTransactions = expected_transactions
    get_merchant_data.formBuild = form_build
    get_merchant_data.ticketSize = ticket_size
    get_merchant_data.avg_ticket_size = avg_ticket_size
    get_merchant_data.loginMasterId = login_id
    get_merchant_data.website_app_url = website_app_url
    get_merchant_data.is_website_url = is_website_url
    get_merchant_data.status = MerchantStatusCode.PENDING.value
    get_merchant_data.save()
    logger(f"merchant data save successfully for login id: {login_id}")
    update_tab_status_by_field(login_id, "business_info_status", KycStatus.PENDING.value)
    return {"status": True, "message": "Merchant data saved successfully"}


def save_settlement_info_other(account_holder_name, account_number, ifsc_code, bank_id, account_type, branch, login_id,
                               modified_by, ):
    check_kyc_status(login_id)
    update_merchant_term_condition_status(login_id)
    try:
        get_merchant_data = merchant_data_by_login_id(login_id)
    except Exception:
        traceback.print_exc()
        raise DataNotFoundException("Merchant data not found for the given login id")
    get_client_data = client_account_details.objects.filter(merchantId=get_merchant_data.merchantId)

    account_details = client_account_details()
    account_details.account_holder_name = account_holder_name
    account_details.merchantId = get_merchant_data.merchantId
    account_details.account_number = account_number
    account_details.ifsc_code = ifsc_code
    account_details.bankId = bank_id
    account_details.modified_by = modified_by
    account_details.accountType = account_type
    account_details.branch = branch
    account_details.is_latest = True
    account_details.login_id = login_service.get_login_master(login_id)

    bank_name = bank_master.objects.get(bankId=bank_id)
    get_merchant_data.bankName = bank_name.bankName
    get_merchant_data.accountNumber = account_number
    get_merchant_data.accountHolderName = account_holder_name
    get_merchant_data.ifscCode = ifsc_code
    get_merchant_data.modifiedDate = datetime.now()
    get_merchant_data.modified_by = login_id
    get_merchant_data.status = MerchantStatusCode.PENDING.value

    if get_client_data.exists():
        get_client_data.update(is_latest=False)
    get_merchant_data.save()
    account_details.save()
    logger(f"merchant data save successfully for login id: {login_id}")
    update_tab_status_by_field(login_id, "settlement_info_status", KycStatus.PENDING.value)
    return {"status": True, "message": "Merchant data saved successfully"}


def get_logo_path_by_id(merchant_id):
    try:
        merchant = merchant_data.objects.get(merchantId=merchant_id)
        return merchant.companyLogoPath
    except Exception:
        traceback.print_exc()
        return None


def get_merchant_address_by_id(login_id):
    try:
        print("Fetching merchant data by login id ", login_id)
        merc_data = merchant_address.objects.get(login_id=login_id)
        return merc_data
    except Exception:
        traceback.print_exc()
        return None


def kyc_submit(login_id, term_condition, submitted_by):
    check_kyc_status(login_id)
    verification = verification_service.get_by_login_id(login_id)
    status = [KycStatus.PENDING.value, KycStatus.VERIFIED.value]
    if verification.general_info_status not in status or verification.merchant_info_status not in status \
            or verification.business_info_status not in status or verification.settlement_info_status not in status:
        raise KycNotFilledException("Please fill all the kyc tabs")
    merchant = validate_required_docs(login_id)
    kyc_submit_data = None
    try:
        kyc_submit_data = get_kyc_consent_date(login_id)
    except Exception:
        traceback.print_exc()
        kyc_submit_data = kyc_consent()
    kyc_submit_data.login_id = login_service.get_login_master(login_id)
    kyc_submit_data.term_condition = term_condition
    kyc_submit_data.submitted_by = login_service.get_login_master(submitted_by)
    kyc_submit_data.updated_on = datetime.now()
    verification.status = KycStatus.PROCESSING.value
    merchant.status = MerchantStatusCode.PROCESSING.value
    merchant.save()
    kyc_submit_data.save()
    verification.save()
    logger(f"kyc submit successfully for login id: {login_id}")
    email_validation(Configuration.get_Property("VERIFIER_EMAIL"), "Verify",
                     Configuration.get_Property("VERIFIER_NAME"),
                     get_login_data(login_id).name,
                     "completed his KYC", "Verify", get_login_data(login_id).username,
                     get_login_data(login_id).mobileNumber)
    return {"status": True, "message": "Kyc submitted successfully"}


def get_login_data(login_id):
    return login_master.objects.get(loginMasterId=login_id)


def save_merchant_address(login_id, address, city, state, pin_code, modified_by):
    state_detail = lookup_state.objects.filter(Q(stateId=state) | Q(stateName=state))
    if not state_detail:
        raise custom_exceptions.StateNameIsIncorrect("Use Correct State Name")
    merchant = None
    try:
        merchant = merchant_address.objects.get(login_id=login_id)
    except Exception:
        traceback.print_exc()
        merchant = merchant_address()
    merchant.login_id = login_service.get_login_master(login_id)
    merchant.address = address
    merchant.city = city
    merchant.state = state
    merchant.pin_code = pin_code
    merchant.submit_by = login_service.get_login_master(modified_by)
    merchant.save()
    logger(f"merchant address save successfully for login id: {login_id}")
    return {"status": True, "message": "Merchant address saved successfully"}


def validate_required_docs(login_id):
    merchant = merchant_data_by_login_id(login_id)
    required_docs = merchant_document_service.get_required_docs(merchant.businessType)
    documents = merchant_document_service.get_merchant_document_by_login_id(login_id)
    merchant_doc_ids = [doc.type.id for doc in documents if doc.status != MerchantDocumentStatus.REJECTED.value]
    print(merchant_doc_ids)
    print(required_docs)
    for doc in required_docs:
        if doc not in merchant_doc_ids:
            print(doc)
            raise KycNotFilledException("Please upload all the required documents")
    return merchant


def merchantData_by_client_code(client_code):
    try:
        return merchant_data.objects.get(clientCode=client_code)
    except Exception as e:
        logger(f"merchant data is not found for the client code {client_code}")
        raise custom_exceptions.ClientNotFound("Client Code Not Found")


def update_merchant_term_condition_status(login_id):
    merchant_consent = None
    try:
        merchant_consent = get_kyc_consent_date(login_id)
    except Exception:
        traceback.print_exc()
        merchant_consent = kyc_consent()
        merchant_consent.created_on = datetime.now()
    merchant_consent.login_id = login_service.get_login_master(login_id)
    merchant_consent.term_condition = False
    merchant_consent.updated_on = datetime.now()
    logger(f"Merchant consent data is updated for login id {login_id}")
    merchant_consent.save()


def check_kyc_status(login_id):
    verification_date = verification_service.get_by_login_id(login_id)
    kyc_status = [KycStatus.VERIFIED.value, KycStatus.APPROVED.value]
    if verification_date.status in kyc_status or verification_date.general_info_status in kyc_status or \
            verification_date.merchant_info_status in kyc_status or verification_date.settlement_info_status in kyc_status or \
            verification_date.business_info_status in kyc_status:
        logger(f"Merchant data is not complete: merchant info status {verification_date.general_info_status}, "
               f"business info status {verification_date.merchant_info_status}, "
               f"business details status {verification_date.business_info_status}, "
               f"bank details status {verification_date.settlement_info_status} ")
        raise KycFilledException("your kyc is under verification")


def get_kyc_consent_date(login_id):
    return kyc_consent.objects.get(login_id=login_id)
