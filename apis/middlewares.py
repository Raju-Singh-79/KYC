import json
import jwt
from rest_framework import status
from django.http import JsonResponse


def log_request(get_response):
    def middleware(request):
        try:
            print("======================= Request body =======================")
            print("Request path : ", request.path)
            print("Request method : ", request.method)
            print("Request content_type : ", request.content_type)
            if request.content_type == 'multipart/form-data':
                for k, v in request.POST.items():
                    print("Request Body :", k + " : " + v)
            elif request.content_type == 'text/plain':
                print("No Body Found....")
            else:
                print("Request Body: ", json.loads(request.body))

        except Exception:
            import traceback
            traceback.print_exc()
        response = get_response(request)
        return response

    return middleware


def JWT_Authentication(get_response):
    def middleware(request):
        allowed_paths = ['/', '/ht/', '/kyc/get-all-business-category/', '/kyc/get-all-state-details/']
        if request.path in allowed_paths:
            response = get_response(request)
            return response
        else:
            try:
                token = request.META.get('HTTP_AUTHORIZATION')
                if token is None:
                    return JsonResponse(
                        {'message': 'Please provide Access token', "status_code": status.HTTP_403_FORBIDDEN,
                         "status": False}, status=status.HTTP_403_FORBIDDEN)
                else:
                    token = token.split()[1]
                if token is None:
                    return JsonResponse(
                        {'message': 'Please provide Access token', "status_code": status.HTTP_403_FORBIDDEN,
                         "status": False}, status=status.HTTP_403_FORBIDDEN)
                data = jwt.decode(token, "6n1wq&1@*mnlt6go%!$0", algorithms="HS256")
                if data['type'] == 'RefreshToken':
                    return JsonResponse(
                        {'message': 'Please provide Access token', "status_code": status.HTTP_403_FORBIDDEN,
                         "status": False}, status=status.HTTP_403_FORBIDDEN)
            except jwt.InvalidSignatureError:
                return JsonResponse(
                    {"message": "Invalid token", "status_code": status.HTTP_403_FORBIDDEN, "status": False},
                    status=status.HTTP_403_FORBIDDEN)
            except jwt.ExpiredSignatureError:
                return JsonResponse(
                    {"message": "expired token", "status_code": status.HTTP_403_FORBIDDEN, "status": False},
                    status=status.HTTP_403_FORBIDDEN)
            except Exception as e:
                import traceback
                traceback.print_exc()
                print("exception", e)
                return JsonResponse(
                    {"message": "Server Error", "status_code": status.HTTP_403_FORBIDDEN, "status": False},
                    status=status.HTTP_403_FORBIDDEN)
            response = get_response(request)
            return response

    return middleware
