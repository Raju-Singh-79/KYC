from apis.database_models.mid_creation import MidCreation
from rest_framework import serializers
from apis.database_models.payement_mode import PaymentMode


class MIDCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MidCreation
        exclude = ("response",)


class PaymentModeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMode
        fields = '__all__'
