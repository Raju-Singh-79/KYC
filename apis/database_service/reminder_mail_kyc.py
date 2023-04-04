from apis.database_models.remainder_mail import ReminderMail
from ..database_service import email_service
from apis.database_models.verification import Verification
from apis.database_models.login_master import login_master
from datetime import date
from apis.enums.kyccodes import KycStatus
import datetime
from ..configuration.config import Configuration

Not_filled = KycStatus.NOT_FILLED.value
Pending = KycStatus.PENDING.value


def send_reminder_configuration():
    get_verification_data = list(Verification.objects.all().values('general_info_status', 'merchant_info_status',
                                                                   'business_info_status', 'settlement_info_status',
                                                                   'login_id'))

    for verification_status in get_verification_data:
        if verification_status['general_info_status'] == Not_filled or verification_status[
            'merchant_info_status'] == Not_filled or verification_status['business_info_status'] == Not_filled or \
                verification_status['settlement_info_status'] == Not_filled:
            try:
                login_data_res = get_login_info(verification_status['login_id'])
            except Exception:
                continue
            create_or_update_reminder_data(login_data_res.loginMasterId, login_data_res.email)

            get_reminder_data = get_reminder_update_data(login_data_res.loginMasterId)
            seven_days_ago = (datetime.datetime.now() - datetime.timedelta(days=7)).date()
            if get_reminder_data.first_attempt == Pending and get_reminder_data.created_date < seven_days_ago:
                send_email_for_kyc_reminder(get_reminder_data.email, login_data_res.name,
                                            verification_status['general_info_status'],
                                            verification_status['merchant_info_status'],
                                            verification_status['settlement_info_status'],
                                            verification_status['business_info_status'])
                create_or_update_column_data(get_reminder_data.login_id, "first_attempt_date", date.today())
                create_or_update_column_data(get_reminder_data.login_id, "first_attempt", "Send")
            elif get_reminder_data.second_attempt == Pending and get_reminder_data.first_attempt_date is not None and get_reminder_data.first_attempt_date < seven_days_ago:
                send_email_for_kyc_reminder(get_reminder_data.email, login_data_res.name,
                                            verification_status['general_info_status'],
                                            verification_status['merchant_info_status'],
                                            verification_status['settlement_info_status'],
                                            verification_status['business_info_status'])
                create_or_update_column_data(get_reminder_data.login_id, "second_attempt_date", date.today())
                create_or_update_column_data(get_reminder_data.login_id, "second_attempt", "Send")

            elif get_reminder_data.third_attempt == Pending and get_reminder_data.second_attempt_date is not None and get_reminder_data.second_attempt_date < seven_days_ago:
                send_email_for_kyc_reminder(get_reminder_data.email, login_data_res.name,
                                            verification_status['general_info_status'],
                                            verification_status['merchant_info_status'],
                                            verification_status['settlement_info_status'],
                                            verification_status['business_info_status'])
                create_or_update_column_data(get_reminder_data.login_id, "third_attempt_date", date.today())
                create_or_update_column_data(get_reminder_data.login_id, "third_attempt", "Send")

    print("reminder mail update as per data")
    return True


def get_login_info(login_id):
    return login_master.objects.get(loginMasterId=login_id, isDirect=True)


def create_or_update_reminder_data(login_id, email):
    try:
        reminder_data = ReminderMail.objects.get(login_id=login_id)
    except Exception:
        reminder_data = ReminderMail()
        reminder_data.created_date = date.today()
    reminder_data.login_id = get_login_info(login_id)
    reminder_data.email = email
    reminder_data.save()


def get_reminder_update_data(login_id):
    print(login_id)
    return ReminderMail.objects.get(login_id=login_id)


def create_or_update_column_data(login_id, field_name, field_value):
    try:
        ReminderMail.objects.filter(login_id=login_id).update(**{field_name: field_value})
    except Exception:
        return None


def send_email_for_kyc_reminder(to, name, general_info, merchant_info, business_info, settlement_info):
    return email_service.email_reminder_validation(to, "kyc-reminder", name,
                                                   "Pending" if general_info == "Not-Filled" else "Completed",
                                                   "Pending" if merchant_info == "Not-Filled" else "Completed",
                                                   "Pending" if business_info == "Not-Filled" else "Completed",
                                                   "Pending" if settlement_info == "Not-Filled" else "Completed",
                                                   "Mandatory", Configuration.get_Property("INTEGRATION_SUPPORT"))
