from django.db import models


class KYCAuditTrails(models.Model):
    id = models.AutoField(primary_key=True)
    merchant_login_id = models.ForeignKey("login_master", on_delete=models.CASCADE, null=False,
                                          db_column="merchant_login_id", unique=True)
    login_id = models.ForeignKey("login_master", on_delete=models.CASCADE, null=True, related_name="login_id",
                                 db_column="login_id")
    merchant_audit_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    remarks = models.TextField(null=True)

    class Meta:
        db_table = "kyc_audit_trails"
