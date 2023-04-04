from django.db import models


class merchant_document(models.Model):
    documentId = models.AutoField(primary_key=True, db_column='document_id')
    merchant = models.ForeignKey('merchant_data', on_delete=models.CASCADE, null=True, db_column='merchantId')
    name = models.CharField(max_length=100, null=True)
    filePath = models.CharField(max_length=255, null=True, db_column='file_Path')
    type = models.ForeignKey('DocumentTypeMaster', on_delete=models.CASCADE, null=True, db_column='type')
    isApproved = models.BooleanField(default=False, db_column='is_Approved')
    approvedDate = models.DateTimeField(null=True, db_column='approved_date')
    approvedBy = models.IntegerField(null=True)
    isLatest = models.BooleanField(null=True, db_column='is_Latest')
    createdDate = models.DateTimeField(null=False, auto_now_add=True, db_column='created_Date')
    createdBy = models.IntegerField(null=True, db_column='created_By')
    modifiedDate = models.DateTimeField(null=True, auto_now=False, db_column='modified_Date')
    modifiedBy = models.IntegerField(null=True, db_column='modified_by')
    status = models.CharField(max_length=50, null=True)
    comment = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'merchant_document'
