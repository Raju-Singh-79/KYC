from django.db import models


class merchant_address(models.Model):
    id = models.AutoField(primary_key=True)
    login_id = models.ForeignKey(
        'apis.login_master', on_delete=models.CASCADE, db_column='login_id')
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    pin_code = models.IntegerField(null=True)
    created_date = models.DateTimeField(null=False, auto_now=True,)
    modified_date = models.DateTimeField(null=False, auto_now=True, db_column='modified_date')
    submit_by = models.ForeignKey('apis.login_master', on_delete=models.CASCADE, db_column='submit_by',
                                  related_name="submit_by")

    class Meta:
        db_table = 'merchant_address'
