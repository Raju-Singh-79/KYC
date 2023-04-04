from enum import Enum


class Role(Enum):
    SUPER_ADMIN = "Super_Admin"
    ADMIN = "Admin"
    BANK = "Bank"
    MERCHANT = "Merchant"
    CLIENT = "Client"
    CUSTOMER = "Customer"
    USER = "User"
    QC_ADMIN = "qcAdmin"
    IP_ADMIN = "ipAdmin"
    SP_ADMIN = "spAdmin"
    SABPAISA_APP = "SabPaisaapp"
    OPERATION_TEAM = "operationTeam"
    RESELLER = "reseller"
    VERIFIER = "verifier"
    APPROVER = "approver"



