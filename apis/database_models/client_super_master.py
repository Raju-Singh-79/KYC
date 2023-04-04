from django.db import models


class client_super_master(models.Model):
    clientId = models.AutoField(primary_key=True, db_column='client_id')
    address = models.CharField(max_length=255, null=True)
    businessType = models.CharField(max_length=45, null=True)
    bid = models.ForeignKey(
        'bank_master', on_delete=models.CASCADE, null=True, db_column='bid')
    clientAuthenticationType = models.CharField(
        max_length=255, null=True, db_column='client_authentication_type')

    clientCode = models.CharField(
        max_length=255, null=True, db_column='client_code')
    clientContact = models.CharField(
        max_length=255, null=True, db_column='client_contact')
    clientEmail = models.CharField(
        max_length=255, null=True, db_column='client_email')
    clientImagePath = models.CharField(
        max_length=255, null=True, db_column='client_image_path')
    clientLink = models.CharField(
        max_length=255, null=True, db_column='client_link')
    clientLogoPath = models.CharField(
        max_length=255, null=True, db_column='client_logo_path')
    clientName = models.CharField(
        max_length=255, null=True, db_column='client_name')
    failedUrl = models.CharField(
        max_length=255, null=True, db_column='failed_url')
    landingPage = models.CharField(
        max_length=255, null=True, db_column='landing_page')
    service = models.CharField(max_length=255, null=True)
    state_id = models.ForeignKey(
        'lookup_state', on_delete=models.CASCADE, null=True, db_column='state_id')
    merchantId = models.IntegerField(null=True, db_column='merchant_id')
    successUrl = models.CharField(
        max_length=255, null=True, db_column='success_url')
    createdDate = models.DateTimeField(null=True, db_column='created_date')
    modifiedDate = models.DateTimeField(null=True, db_column='modified_date')
    modifiedBy = models.IntegerField(null=True, db_column='modified_by')
    status = models.CharField(max_length=50, null=True)
    reason = models.CharField(max_length=255, null=True)
    requestId = models.IntegerField(null=True)
    clientType = models.CharField(
        max_length=45, null=True, db_column='client_type')
    parentClientId = models.IntegerField(
        null=True, db_column='parent_client_id')
    pocAccountManager = models.CharField(
        max_length=150, null=True, db_column='poc_account_manager')

    class Meta:
        db_table = 'client_super_master'
