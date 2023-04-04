from enum import Enum


class MerchantDocumentStatus(Enum):
    SUBMITTED = "Submitted"
    NOT_SUBMITTED = "Not-Submitted"
    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"
    VERIFIED = "Verified"
    NOT_VERIFIED = "Not Verified"
    REMOVED = "Removed"
