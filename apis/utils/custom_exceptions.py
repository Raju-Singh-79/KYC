from rest_framework import status
from rest_framework.exceptions import APIException


class CustomException(Exception):
    """
    Base class for all custom exceptions
    """
    message = None
    status_code = None
    detail = None

    def __init__(self, detail=None, message=None, status_code=None):
        self.message = message or self.message
        self.status_code = status_code or self.status_code
        self.detail = detail or self.detail


class UserAlreadyExistException(CustomException):
    message = "User Already Exist"
    status_code = status.HTTP_409_CONFLICT


class UserNotExistException(CustomException):
    message = "User Not Exist"
    status_code = status.HTTP_404_NOT_FOUND


class UserNotVerifiedException(CustomException):
    message = "Please verify all the KYC information"
    status_code = status.HTTP_400_BAD_REQUEST


class DocumentNotVerifiedException(CustomException):
    message = "Please verify all documents"
    status_code = status.HTTP_400_BAD_REQUEST


class UserNotApprovedException(CustomException):
    message = "User Not Approved"
    status_code = status.HTTP_400_BAD_REQUEST


class UserNotActivatedException(CustomException):
    message = "User Not Activated"
    status_code = status.HTTP_400_BAD_REQUEST


class DataNotFoundException(CustomException):
    message = "Data Not Found"
    status_code = status.HTTP_404_NOT_FOUND


class UnauthorizedException(CustomException):
    message = "Unauthorized"
    status_code = status.HTTP_400_BAD_REQUEST


class IncompleteDataException(CustomException):
    message = "Incomplete Data"
    status_code = status.HTTP_400_BAD_REQUEST


class UnsupportedMediaTypeException(CustomException):
    message = "Unsupported Media Type"
    status_code = status.HTTP_415_UNSUPPORTED_MEDIA_TYPE


class FileTooLargeException(CustomException):
    message = "File Too Large"
    status_code = status.HTTP_413_REQUEST_ENTITY_TOO_LARGE


class FileNotFoundException(CustomException):
    message = "File Not Found"
    status_code = status.HTTP_404_NOT_FOUND


class MoreThenOneRecordException(CustomException):
    message = "More Then One Record Found"
    status_code = status.HTTP_200_OK


class DocumentNotApprovedException(CustomException):
    message = "Document Not Approved"
    status_code = status.HTTP_400_BAD_REQUEST


class DocumentsNotVerifiedException(CustomException):
    message = "Please verify all documents"
    status_code = status.HTTP_400_BAD_REQUEST


class MobileNumberNotVerifiedException(CustomException):
    message = "Mobile Number Not Verified"
    status_code = status.HTTP_400_BAD_REQUEST


class MailNotVerifiedException(CustomException):
    message = "Email Not Verified"
    status_code = status.HTTP_400_BAD_REQUEST


class InvalidApiKeyException(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = {'response_code': status.HTTP_403_FORBIDDEN,
                      'message': 'Invalid Authentication Credentials'}


class MissingAPIKeyException(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = {
        'response_code': status.HTTP_400_BAD_REQUEST,
        'message': 'Authentication Credentials Were Not Provided'
    }


class StateNameIsIncorrect(CustomException):
    message = "State Name Is Incorrect"
    status_code = status.HTTP_400_BAD_REQUEST


class KycNotFilledException(CustomException):
    message = "KYC not filled"
    status_code = status.HTTP_400_BAD_REQUEST


class KycFilledException(CustomException):
    message = "your kyc is under verification"
    status_code = status.HTTP_400_BAD_REQUEST


class ClientNotFound(CustomException):
    message = "Client Code Not Found"
    status_code = status.HTTP_400_BAD_REQUEST


class BankNotFound(CustomException):
    message = "Bank Name Not Found"
    status_code = status.HTTP_404_NOT_FOUND


class BankNotIntegrated(CustomException):
    message = "Bank Is Not Register"
    status_code = status.HTTP_404_NOT_FOUND


class MidCreation(CustomException):
    message = "MID Already Created"
    status_code = status.HTTP_404_NOT_FOUND


class BusinessTypeDataNotFound(CustomException):
    message = "Business Type Data Not Found for This Merchant"
    status_code = status.HTTP_404_NOT_FOUND


class UnauthorizedBankException(CustomException):
    message = "There is an internal server error, please contact with administrator"
    status_code = status.HTTP_400_BAD_REQUEST
