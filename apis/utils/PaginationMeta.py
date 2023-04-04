from rest_framework.pagination import PageNumberPagination
from apis.database_models.login_master import login_master
from apis.database_models.lookup_state import lookup_state
from apis.database_service.client_account_details_service import client_account_details_by_merchant_id
from apis.database_service.merchant_data_service import get_merchant_address_by_id
from apis.database_models.merchant_data import merchant_data


class PaginationMeta(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 10000


def get_custom_merchant_response(data):
    for merchant in data:
        # print(">>>>>>>>>>>>>>>>>>>>>>> :", merchant)
        merchant_list = list(merchant.values())
        # print(">>>>>>>>>>>>>>>>>>>>>>>>merchant_list : ", merchant_list)
        # login_id = merchant_list[24]
        login_id = merchant_list[26]
        print(">>>>>>>>>>>>>>>>>>>>>>>login_id: ", login_id)
        try:
            login = login_master.objects.get(loginMasterId=login_id)
            is_direct = "online" if login.isDirect else "offline"
            created_date = login.createdDate

        except Exception as e:
            is_direct = None
            created_date = None
        try:
            merchant_id = merchant_data.objects.get(loginMasterId=login_id).merchantId
            account_details = client_account_details_by_merchant_id(merchant_id)
            account_type = account_details.accountType
            branch = account_details.branch
        except Exception as e:
            account_type = None
            branch = None
        try:
            address = get_merchant_address_by_id(login_id)
            state_name = lookup_state.objects.get(stateId=address.state).stateName
        except Exception as e:
            state_name = None
        try:
            get_merchant_data = merchant_data.objects.filter(loginMasterId=login_id).values()
            merchant.update(get_merchant_data[0])
        except Exception as e:
            merchant.update({"MerchantData": None})
        merchant.update({"accountType": account_type})
        merchant.update({"branch": branch})
        merchant.update({"state_name": state_name})
        merchant.update({"isDirect": is_direct})
        merchant.update({"signUpDate": created_date})
    return data
