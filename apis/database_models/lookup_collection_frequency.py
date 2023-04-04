from django.db import models


class collection_frequency(models.Model):
    collectionFrequencyId = models.AutoField(primary_key=True)
    collectionFrequencyName = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = 'lookup_collection_frequency'
