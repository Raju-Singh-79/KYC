from enum import Enum


class KycStatus(Enum):
    NOT_FILLED = "Not-Filled"
    PENDING = "Pending"
    PROCESSING = "Processing"
    APPROVED = "Approved"
    VERIFIED = "Verified"
    REJECTED = "Rejected"
    # Incompleted_KYC = "Incompleted KYC"


