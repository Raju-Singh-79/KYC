from pyexpat import model
from django.db import models


class kyc_consent(models.Model):
    id = models.AutoField(primary_key=True)
    login_id = models.ForeignKey('apis.login_master', on_delete=models.CASCADE, db_column='login_id')
    term_condition = models.BooleanField(null=True)
    submitted_by = models.ForeignKey('apis.login_master', on_delete=models.CASCADE, db_column='submitted_by',
                                     related_name="submitted_by")
    created_on = models.DateTimeField(null=True, auto_now=False, db_column="created_on")
    updated_on = models.DateTimeField(null=True, auto_now=False, db_column="updated_on")

    class Meta:
        db_table = 'kyc_consent'
