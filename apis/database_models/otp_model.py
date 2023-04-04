import uuid
from django.db import models
from apis.enums.otpcodes import OtpStatus


class OTP(models.Model):
    id = models.AutoField(primary_key=True)
    otp = models.CharField(max_length=6, null=True)
    verification_token = models.CharField(
        max_length=100, default=str(uuid.uuid4()).replace('-', ''))
    mobile_number = models.CharField(max_length=10, null=True)
    email = models.EmailField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_expired = models.BooleanField(default=False)
    status = models.CharField(max_length=40, default=OtpStatus.PENDING.value)
    otp_for = models.CharField(max_length=40, null=False)
    otp_type = models.CharField(max_length=40, null=False)

    class Meta:
        db_table = 'otp'
