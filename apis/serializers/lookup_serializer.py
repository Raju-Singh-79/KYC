from rest_framework import serializers
from ..database_models.lookup_state import lookup_state
from ..database_models.lookup_business_type import business_type
from ..database_models.lookup_platform import platform
from ..database_models.lookup_collection_frequency import collection_frequency
from ..database_models.lookup_collection_type import collection_type
from ..database_models.bank_master import bank_master
from ..database_models.lookup_business_category import business_category
from ..database_models.lookup_role import lookup_role
from ..database_models.risk_category_master import risk_category_master


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = lookup_state
        fields = '__all__'


class BusinessTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = business_type
        fields = '__all__'


class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = platform
        fields = '__all__'


class CollectionFrequencySerializer(serializers.ModelSerializer):
    class Meta:
        model = collection_frequency
        fields = '__all__'


class CollectionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = collection_type
        fields = '__all__'


class BankNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = bank_master
        fields = ('bankId', 'bankName')


class BusinessCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = business_category
        fields = '__all__'


class LookupRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = lookup_role
        fields = ['roleId', 'roleName']


class RiskCategoryMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = risk_category_master
        fields = ['risk_category_code', 'risk_category_name']

