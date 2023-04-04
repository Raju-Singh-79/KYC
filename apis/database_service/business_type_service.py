from ..serializers.lookup_serializer import BusinessTypeSerializer
from ..database_models.lookup_business_type import business_type
from apis.utils.custom_exceptions import DataNotFoundException


def business_type_details():
    get_business_type_data = business_type.objects.all()
    return BusinessTypeSerializer(get_business_type_data, many=True).data


def business_type_details_by_id(business_type_id):
    get_business_type_data = business_type.objects.filter(businessTypeId=business_type_id)
    return BusinessTypeSerializer(get_business_type_data, many=True).data
