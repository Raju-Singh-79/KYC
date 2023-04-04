from django.db import models


class collection_type(models.Model):
    collectionTypeId = models.AutoField(primary_key=True)
    collectionTypeName = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = 'lookup_collection_Type'
