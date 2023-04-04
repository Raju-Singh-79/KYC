from django.db import models


class platform(models.Model):
    platformId = models.AutoField(primary_key=True)
    platformName = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = 'lookup_platform'
