from rest_framework import serializers
from ..database_models.client_account_details import client_account_details


class ClientAccountDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = client_account_details
        fields = '__all__'
