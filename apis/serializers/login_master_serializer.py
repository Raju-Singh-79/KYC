from ..database_models.login_master import login_master 
from rest_framework import serializers

class login_master_serializer(serializers.ModelSerializer):
    class Meta:
        model = login_master
        fields = '__all__'