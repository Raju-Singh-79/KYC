from ..serializers.lookup_serializer import StateSerializer
from ..database_models.lookup_state import lookup_state


def all_state_service():
    get_lookupstate_data = lookup_state.objects.all()
    lookupstate_response = StateSerializer(get_lookupstate_data, many=True).data
    return lookupstate_response
