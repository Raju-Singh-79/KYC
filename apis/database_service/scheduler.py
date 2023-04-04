from apscheduler.schedulers.background import BackgroundScheduler
from apis.database_service.reminder_mail_kyc import send_reminder_configuration

scheduler = BackgroundScheduler()
scheduler.add_job(send_reminder_configuration, 'interval', days=1)
try:
    scheduler.start()
except (KeyboardInterrupt, SystemExit):
    pass
