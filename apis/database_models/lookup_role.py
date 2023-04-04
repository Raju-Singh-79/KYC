from django.db import models


class lookup_role(models.Model):
    roleId = models.AutoField(primary_key=True, db_column='role_id')
    roleName = models.CharField(
        max_length=50, null=True, db_column='role_name')

    class Meta:
        db_table = 'lookup_role'
