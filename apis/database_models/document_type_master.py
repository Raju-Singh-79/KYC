from django.db import models


class DocumentTypeMaster(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=100)

    class Meta:
        db_table = 'document_type_master'
