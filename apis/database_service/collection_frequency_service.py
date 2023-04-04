from ..serializers.lookup_serializer import CollectionFrequencySerializer
from ..database_models.lookup_collection_frequency import collection_frequency


def collection_frequency_service():
    get_collection_frequency_data = collection_frequency.objects.all()
    collection_frequency_response = CollectionFrequencySerializer(
        get_collection_frequency_data, many=True).data
    return collection_frequency_response
