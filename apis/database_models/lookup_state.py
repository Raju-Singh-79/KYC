from django.db import models


class lookup_state(models.Model):
    stateId = models.AutoField(primary_key=True, db_column='state_id')
    stateCode = models.CharField(
        max_length=50, null=True, db_column='state_code')
    stateName = models.CharField(
        max_length=50, null=True, db_column='state_name')

    class Meta:
        db_table = 'lookup_state'
