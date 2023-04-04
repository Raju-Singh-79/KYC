from datetime import datetime

from rest_framework import serializers

from apis.database_models.verification import Verification
from apis.enums.kyccodes import KycStatus


class VerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Verification
        fields = "__all__"
        write_only_fields = (
            "login_id",
            "approved_by",
            "general_info_verified_by",
            "merchant_info_verified_by",
            "business_info_verified_by",
            "settlement_info_verified_by",
        )

    def validate(self, data):
        if data.get("general_info_verified_by"):
            data["general_info_verified_date"] = datetime.now()
            data["general_info_status"] = KycStatus.VERIFIED.value
        elif data.get("merchant_info_verified_by"):
            data["merchant_info_verified_date"] = datetime.now()
            data["merchant_info_status"] = KycStatus.VERIFIED.value
        elif data.get("business_info_verified_by"):
            data["business_info_verified_date"] = datetime.now()
            data["business_info_status"] = KycStatus.VERIFIED.value
        elif data.get("settlement_info_verified_by"):
            data["settlement_info_verified_date"] = datetime.now()
            data["settlement_info_status"] = KycStatus.VERIFIED.value
        else:
            raise serializers.ValidationError("Verified by field is required")
        return data


class VerificationDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Verification
        fields = "__all__"
