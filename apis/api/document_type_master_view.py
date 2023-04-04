import traceback
from rest_framework import viewsets
from rest_framework.response import Response
from django.forms.models import model_to_dict
from apis.serializers.document_type_master_serializer import DocumentTypeMasterSerializer
from apis.database_models.document_type_master import DocumentTypeMaster
from apis.database_models.business_doc_type_mapper import business_doc_type_mapper


class DocumentTypeMasterAPI(viewsets.ViewSet):
    queryset = DocumentTypeMaster.objects.all()

    def list(self, request):
        business_type_id = request.query_params.get("business_type_id")
        try:
            get_business_id_by_mapper = business_doc_type_mapper.objects.filter(
                business_type_id=business_type_id).values()
            data = []
            for i in range(len(get_business_id_by_mapper)):
                doc_type = DocumentTypeMaster.objects.get(id=get_business_id_by_mapper[i].get('doc_type_id'))
                model_doc_type = model_to_dict(doc_type)
                serialize_doc_type = DocumentTypeMasterSerializer(model_doc_type).data
                serialize_doc_type["is_required"] = get_business_id_by_mapper[i].get('is_required')
                data.append(serialize_doc_type)
            return Response(data)
        except Exception as e:
            traceback.print_exc()
            return None
