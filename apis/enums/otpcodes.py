from enum import Enum


class OtpStatus(Enum):
    PENDING = "Pending"
    VERIFIED = "Verified"
    EXPIRED = "Expired"


class OtpType(Enum):
    PHONE = "Phone"
    EMAIL = "Email"
