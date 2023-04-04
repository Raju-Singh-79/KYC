from django.db import models


class TempKyc(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    login_id = models.IntegerField(null=True, db_column='login_id')
    name = models.CharField(max_length=255, null=True, db_column='name')
    number = models.CharField(max_length=255, null=True, db_column='number')
    email = models.CharField(max_length=255, null=True, db_column='email')
    designation = models.CharField(
        max_length=255, null=True, db_column='designation')
    business_type = models.IntegerField(null=True, db_column='business_type')
    business_category = models.IntegerField(
        null=True, db_column='business_category')
    business_model = models.CharField(
        max_length=255, null=True, db_column='business_model')
    billing_label = models.CharField(
        max_length=255, null=True, db_column='billing_label')
    is_erp_owner = models.BooleanField(default=False, db_column='is_erp_owner')
    platform = models.CharField(
        max_length=255, null=True, db_column='platform')
    website_url = models.CharField(
        max_length=255, null=True, db_column='website_url')
    collection_type = models.IntegerField(
        null=True, db_column='collection_type')
    collection_frequency = models.IntegerField(
        null=True, db_column='collection_frequency')
    ticket_size = models.CharField(
        max_length=255, null=True, db_column='ticket_size')
    expected_transactions = models.CharField(
        max_length=255, null=True, db_column='expected_transactions')
    sabpaisa_form = models.BooleanField(
        default=False, db_column='sabpaisa_form')
    business_name = models.CharField(
        max_length=255, null=True, db_column='business_name')
    logo_path = models.CharField(
        max_length=255, null=True, db_column='logo_path')
    gstin = models.CharField(max_length=255, null=True, db_column='gstin')
    business_pan = models.CharField(
        max_length=255, null=True, db_column='business_pan')
    authorized_signatory = models.CharField(
        max_length=255, null=True, db_column='authorized_signatory')
    name_on_pan = models.CharField(
        max_length=255, null=True, db_column='name_on_pan')
    pin_code = models.CharField(
        max_length=255, null=True, db_column='pin_code')
    city = models.CharField(max_length=255, null=True, db_column='city')
    state = models.CharField(max_length=255, null=True,
                             db_column='lookup_state')
    registered_address = models.CharField(
        max_length=255, null=True, db_column='registered_address')
    operational_address = models.CharField(
        max_length=255, null=True, db_column='operational_address')
    account_name = models.CharField(
        max_length=255, null=True, db_column='account_name')
    account_type = models.CharField(
        max_length=255, null=True, db_column='account_type')
    bank_name = models.CharField(
        max_length=255, null=True, db_column='bank_name')
    branch = models.CharField(max_length=255, null=True, db_column='branch')
    ifsc_code = models.CharField(
        max_length=255, null=True, db_column='ifsc_code')
    account_number = models.CharField(
        max_length=255, null=True, db_column='account_number')
    is_kyc_complete = models.BooleanField(
        default=False, db_column='is_kyc_complete')
    is_kyc_approved = models.BooleanField(
        default=False, db_column='is_kyc_approved')
    kyc_approved_by = models.IntegerField(
        null=True, db_column='kyc_approved_by')
    kyc_approved_date = models.DateTimeField(
        null=True, db_column='kyc_approved_date')
    kyc_rejected_by = models.IntegerField(
        null=True, db_column='kyc_rejected_by')
    kyc_rejected_date = models.DateTimeField(
        null=True, db_column='kyc_rejected_date')
    kyc_rejected_reason = models.CharField(
        max_length=255, null=True, db_column='kyc_rejected_reason')
    created_on = models.DateTimeField(
        auto_now_add=True, db_column='created_on')
    updated_on = models.DateTimeField(auto_now=True, db_column='updated_on')
    created_by = models.CharField(
        max_length=255, null=True, db_column='created_by')
    updated_by = models.CharField(
        max_length=255, null=True, db_column='updated_by')
    kyc_status = models.CharField(
        max_length=50, null=True, db_column='kyc_status')

    class Meta:
        db_table = 'temp_kyc'
