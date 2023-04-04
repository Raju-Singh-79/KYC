from django.db import models


class login_master(models.Model):
    loginMasterId = models.AutoField(primary_key=True, db_column='login_master_id')
    name = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=255, null=True)
    mobileNumber = models.CharField(max_length=255, null=True, db_column='mobile_number')
    password = models.CharField(max_length=255, null=True)
    username = models.CharField(max_length=255, null=True)
    account_details_client_account_id = models.ForeignKey('client_account_details', on_delete=models.CASCADE,
                                                          null=True, db_column='acount_details_client_account_id')
    master_client_id = models.ForeignKey('client_super_master', on_delete=models.CASCADE, null=True,
                                         db_column='master_client_id')
    roleId = models.ForeignKey('lookup_role', on_delete=models.CASCADE, null=True, db_column='role_id')
    createdDate = models.DateTimeField(auto_now_add=True, null=True, db_column='created_date')
    modifiedDate = models.DateTimeField(null=True, db_column='modified_date')
    modifiedBy = models.IntegerField(null=True, db_column='modified_by')
    status = models.CharField(max_length=50, default='Pending')
    reason = models.CharField(max_length=255, null=True)

    lastLoginTime = models.DateTimeField(null=True, db_column='last_login_time')

    requestId = models.IntegerField(null=True)
    requestedClientType = models.CharField(max_length=45, null=True, db_column='requested_client_type')
    requestedParentClientId = models.IntegerField(null=True, db_column='requested_parent_client_id')
    # referrer_code = models.CharField(max_length=255, null=True, db_column='referrer_code')
    isDirect = models.BooleanField(null=False, default=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'login_master'
