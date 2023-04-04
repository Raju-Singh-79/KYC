from enum import Enum


class ApiKeyStatus(Enum):
    ACTIVE = 'Active'
    INACTIVE = 'Inactive'
    BLOCKED = 'Blocked'