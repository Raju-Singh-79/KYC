from django.db import models


class risk_category_master(models.Model):
    id = models.AutoField(primary_key=True)
    risk_category_code = models.CharField(max_length=100)
    risk_category_name = models.CharField(max_length=100)
    Description = models.CharField(max_length=300)
    is_active = models.BooleanField(default=False)

    class Meta:
        db_table = 'risk_category_master'
