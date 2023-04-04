from django.db import models


class business_type(models.Model):
    businessTypeId = models.AutoField(primary_key=True)
    businessTypeText = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = 'lookup_business_type'
