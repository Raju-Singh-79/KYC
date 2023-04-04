from django.db import models


class business_doc_type_mapper(models.Model):
    id = models.AutoField(primary_key=True)
    business_type_id = models.CharField(max_length=255, null=True)
    doc_type_id = models.CharField(max_length=255, null=True)
    is_required = models.BooleanField(default=False)

    class Meta:
        db_table = 'business_doc_type_mapper'
