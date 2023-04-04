from pyexpat import model
from rest_framework import serializers
from ..database_models.merchant_address import merchant_address


class MerchantAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = merchant_address
        fields = '__all__'
