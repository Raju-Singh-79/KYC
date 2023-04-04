from rest_framework import permissions
from apis.database_models.ApiKey import ApiKey
from apis.enums.apikeycodes import ApiKeyStatus
from apis.utils.custom_exceptions import MissingAPIKeyException, InvalidApiKeyException


class ApiKeyPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        authorization = request.META.get('HTTP_AUTHORIZATION', None)
        if not authorization:
            raise MissingAPIKeyException()
        key = ApiKey.objects.filter(
            key=authorization, status=ApiKeyStatus.ACTIVE.value).exists()
        if not key:
            raise InvalidApiKeyException()
        return True
