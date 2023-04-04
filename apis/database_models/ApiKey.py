import uuid
from django.db import models


class ApiKey(models.Model):
    id = models.AutoField(primary_key=True)
    key = models.CharField(max_length=255, default=uuid.uuid4())
    assigned_to = models.CharField(max_length=255, null=False)
    status = models.CharField(max_length=255, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'api_key'
