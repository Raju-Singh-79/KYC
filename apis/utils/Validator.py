from apis.configuration.config import Configuration
from apis.utils.custom_exceptions import IncompleteDataException, UnsupportedMediaTypeException, FileTooLargeException
import requests


def validate_request_data(fields: list, request_data):
    for key in fields:
        if not (key in request_data and request_data[key]):
            raise IncompleteDataException("{} is missing".format(key))
    return {"status": True, "message": "Data validated successfully"}


def validate_file(logo):
    if logo.content_type not in ['image/jpeg', 'image/png']:
        raise UnsupportedMediaTypeException("Unsupported media type")
    if (logo.size / (1024 * 1024)) > int(Configuration.get_Property("MAX_FILE_SIZE")):
        raise FileTooLargeException("File size is too large")
    return {"status": True, "message": "Logo validated successfully"}


def send_request(url, data, headers=None, type=None):
    headers['Content-Type'] = 'application/json'
    print("sending request...")
    if type == 'POST':
        res = requests.post(url, json=data, headers=headers)
    elif type == 'GET':
        res = requests.get(url, json=data, headers=headers)
    print("request sent")
    return res
