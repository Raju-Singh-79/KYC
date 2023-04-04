import traceback

from apis.database_models.lookup_role import lookup_role
from apis.database_models.login_master import login_master
from apis.serializers.lookup_serializer import LookupRoleSerializer
from apis.database_models.risk_category_master import risk_category_master
from apis.serializers.lookup_serializer import RiskCategoryMasterSerializer
from apis.database_service.logger import logger


def get_role_id(role_name):
    try:
        role_id = lookup_role.objects.get(role_name=role_name).id
        return role_id
    except Exception:
        logger(f"role data is not for {role_name}")
        return None


def get_role(role_id):
    try:
        return lookup_role.objects.get(roleId=role_id)
    except Exception:
        traceback.print_exc()
        logger(f"{role_id}  is not authorized to perform this action")
        return None


def check_role_access(role, roles):
    role_name = role.roleName.lower()
    if role_name in [role.lower() for role in roles]:
        return True
    else:
        logger(f"{role_name}  is not authorized to perform this action")
        return False


def get_role_by_login_id(login_id):
    try:
        role = login_master.objects.get(loginMasterId=login_id).roleId
        return role
    except Exception:
        logger(f"{login_id} is not found for the role")
        return None


def get_role_id_and_name(req):
    try:
        role_data = lookup_role.objects.all()
        return LookupRoleSerializer(role_data, many=True).data
    except Exception:
        return None


def get_risk_category_data(req):
    try:
        risk_category_data = risk_category_master.objects.filter(is_active=True)
        return RiskCategoryMasterSerializer(risk_category_data, many=True).data
    except Exception:
        return None
