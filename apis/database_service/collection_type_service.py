from ..serializers.lookup_serializer import CollectionTypeSerializer
from ..database_models.lookup_collection_type import collection_type


def collection_type_data():
    get_collection_type_data = collection_type.objects.all()
    collectiontype_response = CollectionTypeSerializer(
        get_collection_type_data, many=True).data
    return collectiontype_response
