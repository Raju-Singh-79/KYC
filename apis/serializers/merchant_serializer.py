from rest_framework import serializers
from ..database_models.merchant_data import merchant_data
from ..database_models.kyc_consent import kyc_consent


class MerchantData(serializers.ModelSerializer):
    names = serializers.CharField(max_length=250)

    class Meta:
        model = merchant_data
        fields = ('merchantId', 'name', 'names')


class MerchantDocumentById(serializers.ModelSerializer):
    OriginialFilePath = serializers.CharField(max_length=250)

    class Meta:
        model = merchant_data
        fields = ('merchantId', 'name',
                  'OriginialFilePath', 'type', 'isApproved')


class merchant_data_serializer(serializers.ModelSerializer):
    class Meta:
        model = merchant_data
        fields = '__all__'


class MerchantConsent(serializers.ModelSerializer):
    class Meta:
        model = kyc_consent
        fields = ('login_id', 'term_condition')
