from django.db import models


class MidCreation(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    client_code = models.CharField(max_length=255, null=True, db_column='client_code')
    bank_id = models.ForeignKey("bank_master", on_delete=models.CASCADE, null=True, db_column='bank_id')
    payment_mode = models.CharField(max_length=255, null=True, db_column='payment_mode')
    sub_merchant_id = models.CharField(max_length=255, null=True, db_column='sub_merchant_id')
    created_date = models.DateTimeField(null=True)
    modified_date = models.DateTimeField(null=True)
    is_active = models.BooleanField(default=True)
    response = models.JSONField(null=True)

    class Meta:
        db_table = 'mid_creation'



