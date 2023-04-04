from ..serializers.lookup_serializer import BusinessCategorySerializer
from ..database_models.lookup_business_category import business_category


def business_category_details():
    get_business_category_data = business_category.objects.all()
    return BusinessCategorySerializer(get_business_category_data, many=True).data


def business_category_details_by_id(category_id):
    get_business_category_data = business_category.objects.filter(category_id=category_id)
    return BusinessCategorySerializer(get_business_category_data, many=True).data

