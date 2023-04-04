from ..serializers.lookup_serializer import PlatformSerializer
from ..database_models.lookup_platform import platform

def platform_data():
        get_platform_type_data = platform.objects.all()
        platofrm_type_response = PlatformSerializer(get_platform_type_data, many = True).data
        return platofrm_type_response
    
    