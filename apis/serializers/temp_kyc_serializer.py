# from rest_framework import serializers
# from rest_framework.serializers import ModelSerializer
#
# from apis.database_models.temp_kyc import TempKyc
#
#
# class KycSerializer(ModelSerializer):
#     files = serializers.FileField(max_length=250, allow_empty_file=False, use_url=False, write_only=True, required=False)
#     logo = serializers.FileField(max_length=250, allow_empty_file=False, use_url=False, write_only=True, required=False)
#
#     class Meta:
#         model = TempKyc
#         fields = '__all__'
#
#
# class TempKycSerializer(ModelSerializer):
#     class Meta:
#         model = TempKyc
#         fields = '__all__'
#         read_only_fields = ('id',)