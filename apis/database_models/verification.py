from django.db import models
from apis.enums.kyccodes import KycStatus


class Verification(models.Model):
    id = models.AutoField(primary_key=True)
    login_id = models.ForeignKey("login_master", on_delete=models.CASCADE, null=False, db_column="login_id")
    approved_by = models.ForeignKey("login_master", on_delete=models.CASCADE, null=True, related_name="approved_by",
                                    db_column="approved_by")
    approved_date = models.DateTimeField(null=True)
    verified_date = models.DateTimeField(null=True)
    is_approved = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    general_info_status = models.CharField(max_length=100, null=True, default=KycStatus.NOT_FILLED.value)
    merchant_info_status = models.CharField(max_length=100, null=True, default=KycStatus.NOT_FILLED.value)
    business_info_status = models.CharField(max_length=100, null=True, default=KycStatus.NOT_FILLED.value)
    settlement_info_status = models.CharField(max_length=100, null=True, default=KycStatus.NOT_FILLED.value)
    general_info_verified_by = models.ForeignKey("login_master", on_delete=models.CASCADE,
                                                 related_name="general_info_verified_by",
                                                 null=True, db_column="general_info_verified_by")
    merchant_info_verified_by = models.ForeignKey("login_master", on_delete=models.CASCADE,
                                                  related_name="merchant_info_verified_by",
                                                  null=True, db_column="merchant_info_verified_by")
    business_info_verified_by = models.ForeignKey("login_master", on_delete=models.CASCADE,
                                                  related_name="business_info_verified_by",
                                                  null=True, db_column="business_info_verified_by")
    settlement_info_verified_by = models.ForeignKey("login_master", on_delete=models.CASCADE,
                                                    related_name="settlement_info_verified_by",
                                                    null=True, db_column="settlement_info_verified_by")
    general_info_verified_date = models.DateTimeField(null=True)
    merchant_info_verified_date = models.DateTimeField(null=True)
    business_info_verified_date = models.DateTimeField(null=True)
    settlement_info_verified_date = models.DateTimeField(null=True)
    general_info_reject_comments = models.TextField(null=True)
    merchant_info_reject_comments = models.TextField(null=True)
    business_info_reject_comments = models.TextField(null=True)
    settlement_info_reject_comments = models.TextField(null=True)
    general_info_reject_date = models.DateTimeField(null=True)
    merchant_info_reject_date = models.DateTimeField(null=True)
    business_info_reject_date = models.DateTimeField(null=True)
    settlement_info_reject_date = models.DateTimeField(null=True)
    kyc_reject = models.DateTimeField(null=True)
    comments = models.TextField(null=True)
    status = models.CharField(max_length=100, null=True, default=KycStatus.NOT_FILLED.value)

    class Meta:
        db_table = "verification"
