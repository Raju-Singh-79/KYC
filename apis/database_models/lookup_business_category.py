from django.db import models


class business_category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = 'lookup_business_category'
