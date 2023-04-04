from apis.database_models.login_master import login_master
from apis.utils.custom_exceptions import DataNotFoundException, UserAlreadyExistException


def get_login_master(login_id):
    try:
        return login_master.objects.get(loginMasterId=login_id)
    except login_master.DoesNotExist:
        raise DataNotFoundException("User not found for the given login id")


def get_by_email(email: str) -> login_master:
    try:
        return login_master.objects.get(email=email)
    except login_master.DoesNotExist:
        raise DataNotFoundException("Login data not found for the given email")


def get_by_mobile(mobile: str) -> login_master:
    try:
        return login_master.objects.get(mobileNumber=mobile)
    except login_master.DoesNotExist:
        raise DataNotFoundException(
            "Login data not found for the given mobile number")
