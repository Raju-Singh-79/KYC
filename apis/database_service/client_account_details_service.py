from apis.utils import custom_exceptions
from ..database_models.client_account_details import client_account_details
from ..serializers import client_account_serializer


def get_client_account_details(data):
    try:
        merchant_id = data.get('merchant_id')
        login_id = data.get('login_id')

        if merchant_id and login_id:
            merchant_and_login_id_data = client_account_details.objects.get(merchantId=merchant_id, login_id=login_id,
                                                                            is_latest=True)
            respnse_by_merchant_login = client_account_serializer.ClientAccountDetailSerializer(
                merchant_and_login_id_data).data
            return respnse_by_merchant_login
        elif merchant_id:
            merchant_id_data = client_account_details.objects.get(
                merchantId=merchant_id, is_latest=True)
            response_by_merhcant_id = client_account_serializer.ClientAccountDetailSerializer(
                merchant_id_data).data
            return response_by_merhcant_id

        elif login_id:
            login_id_data = client_account_details.objects.get(
                login_id=login_id, is_latest=True)
            response_by_login_id = client_account_serializer.ClientAccountDetailSerializer(
                login_id_data).data
            return response_by_login_id
        else:
            raise custom_exceptions.DataNotFoundException(
                "merchant_id & login_id is required")
    except client_account_details.DoesNotExist:
        return {"status": False, "message": "Invalid login_id or merchant_id"}


def client_account_details_by_merchant_id(merchant_id):
    try:
        return client_account_details.objects.get(merchantId=merchant_id, is_latest=True)
    except Exception:
        raise custom_exceptions.DataNotFoundException("Client account details not found")
