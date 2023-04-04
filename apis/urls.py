from django.urls import path, include
from rest_framework import routers

from apis.api import kyc_view
from apis.api import merchant_data_view
from apis.api import state_api, business_type, platform_api, collection_frequency, collection_type, bank_name, \
    business_category, mid_creation_api
from apis.api.client_account_detail_api import client_account_details
from apis.api.client_details import client_super_master
from apis.api.document_type_master_view import DocumentTypeMasterAPI
from apis.api.merchant_document_view import MerchantDocumentAPI, get_merchant_doc, get_merchant_logo_by_id
from apis.api.otp_view import OtpView, validate_otp
from apis.api import role_view
from apis.database_service.reminder_mail_kyc import send_reminder_configuration

router = routers.DefaultRouter()
router.register(r'document-type', DocumentTypeMasterAPI, basename='get_document_type')
router.register(r'upload-merchant-document', MerchantDocumentAPI, basename='upload_merchant_document')
router.register(r'send-otp', OtpView, basename='send_otp')
router.register(r'verify-kyc', kyc_view.VerificationApi, basename='verify-kyc')
router.register(r'get-merchant-data', merchant_data_view.MerchantApi, basename='get-merchant-data')
router.register(r'reverse-kyc', kyc_view.ReverseKYC, basename='reverse-kyc')
router.register(r'refer-zone', kyc_view.ReferZone, basename='refer-zone')
router.register(r'mid-creation', mid_creation_api.SubMerchantMidCreation, basename='mid-creation')

urlpatterns = [
    path('getMerchantData/', merchant_data_view.GetMerchantData.as_view()),
    path('GetMerchantDocumentByID/<int:Id>', merchant_data_view.GetMerchantDocumentByID.as_view()),
    path('get-merchant-document/', get_merchant_doc),
    path('', include(router.urls)),
    path('verify-otp/', validate_otp),

    path('save-general-info/', kyc_view.save_general_info_api),
    path('save-merchant-info/', kyc_view.save_merchant_info_api),
    path('save-business-info/', kyc_view.save_business_info_api),
    path('save-settlement-info/', kyc_view.save_settlement_info_api),
    path('kyc-submit/', kyc_view.kyc_consent_api),

    path('download-logo/', get_merchant_logo_by_id),
    path('merchant-data-by-client-code/', merchant_data_view.merchant_data_by_client_code),
    path('merchant-data-by-login-id/', merchant_data_view.merchant_data_by_login_id),
    path('get-client-account-details/', client_account_details),
    path('get-all-client-code/', client_super_master),
    path('get-all-role-details/', role_view.role_data_api),
    path('get-risk-category-details/', role_view.risk_category_data_api),
    path('send-reminder-for-kyc-pending/', send_reminder_configuration, name='send_reminder'),

    ######################################################################
    path('get-all-state-details/', state_api.state_details_api),
    path('get-all-business-type/', business_type.business_type_api),
    path('get-all-platform-type/', platform_api.platform_type_api),
    path('get-all-collection-frequency/', collection_frequency.collection_frequency_api),
    path('get-all-collection-type/', collection_type.collection_type_api),
    path('get-all-bank-name/', bank_name.all_bank_details_api),
    path('get-bank-id-by-name/', bank_name.get_bank_id_api),
    path('get-all-business-category/', business_category.business_category_api),
    path('get-business-category-by-id/', business_category.business_category_by_id),
    path('get-business-type-by-id/', business_type.business_type_by_id),

]
