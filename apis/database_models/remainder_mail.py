from django.db import models
from apis.enums.kyccodes import KycStatus


class ReminderMail(models.Model):
    id = models.AutoField(primary_key=True)
    login_id = models.ForeignKey("login_master", on_delete=models.CASCADE, null=False, db_column="login_id")
    email = models.CharField(max_length=255, null=True)
    first_attempt = models.CharField(max_length=100, null=True, default=KycStatus.PENDING.value)
    second_attempt = models.CharField(max_length=100, null=True, default=KycStatus.PENDING.value)
    third_attempt = models.CharField(max_length=100, null=True, default=KycStatus.PENDING.value)
    first_attempt_date = models.DateField(auto_now=False, blank=True, null=True)
    second_attempt_date = models.DateField(auto_now=False, blank=True, null=True)
    third_attempt_date = models.DateField(auto_now=False, blank=True, null=True)
    created_date = models.DateField(auto_now=False, blank=True, null=True)

    class Meta:
        db_table = 'reminder_mail'
