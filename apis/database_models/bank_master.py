from django.db import models


class bank_master(models.Model):
    bankId = models.AutoField(primary_key=True, db_column='bank_id')
    bankCode = models.CharField(
        max_length=255, null=True, db_column='bank_code')
    bankLogoPath = models.CharField(
        max_length=255, null=True, db_column='bank_logo_path')
    bankName = models.CharField(
        max_length=255, null=True, db_column='bank_name')
    loginId = models.CharField(max_length=200, db_column='loginId')
    bank_Id = models.IntegerField(null=True, db_column='bankId')

    class Meta:
        db_table = 'bank_master'
