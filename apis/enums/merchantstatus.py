from enum import Enum


class MerchantStatusCode(Enum):
    ACTIVATED = "Activated"
    DEACTIVATED = "Deactivated"
    BLOCKED = "Blocked"
    NOT_FILLED = "Not-Filled"
    REJECTED = "Rejected"
    PENDING = "Pending"
    PROCESSING = "Processing"
    REQUESTED = "Requested"
    INCOMPLETE_KYC = "Incomplete KYC"
    APPROVED = "Approved"
    VERIFIED = "Verified"
    NOT_VERIFIED = "Not Verified"
    KYC_NOT_INITIATED = "KYC Not Initiated"
