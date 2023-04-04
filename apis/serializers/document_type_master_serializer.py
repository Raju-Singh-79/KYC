from apis.database_models.document_type_master import DocumentTypeMaster
from rest_framework import serializers


class DocumentTypeMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentTypeMaster
        fields = '__all__'
