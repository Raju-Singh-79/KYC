from apis.database_models.merchant_document import merchant_document
from rest_framework import serializers


class MerchantDocumentSerializer(serializers.ModelSerializer):
    files = serializers.FileField(max_length=250, allow_empty_file=False, use_url=False, write_only=True, required=True)
    login_id = serializers.CharField(max_length=50, allow_null=False, allow_blank=False, required=True, write_only=True)

    class Meta:
        model = merchant_document
        fields = '__all__'


class MerchantAadharSerializer(serializers.ModelSerializer):
    aadhar_front = serializers.FileField(max_length=250, allow_empty_file=False, use_url=False, write_only=True, required=True)
    aadhar_back = serializers.FileField(max_length=250, allow_empty_file=False, use_url=False, write_only=True, required=True)
    login_id = serializers.CharField(max_length=50, allow_null=False, allow_blank=False, required=True, write_only=True)

    class Meta:
        model = merchant_document
        fields = '__all__'
