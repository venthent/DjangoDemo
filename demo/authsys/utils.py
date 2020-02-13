import logging, os, datetime
from logging.handlers import RotatingFileHandler

import jwt
from rest_framework import status
from django.http import JsonResponse

from .models import Emp, Org, JWT_SECRET_KEY

logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('emp: '
                              '"%(message)s"'
                              )
log_path = os.path.join(os.getcwd(), "logs", "emp.log")
file_handler = RotatingFileHandler(log_path, maxBytes=1024 * 1024 * 100, backupCount=10)
# file_handler = StreamHandler()
# file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def logger_decorator(func):
    """A decorator for log"""

    def wrapper(*args, **kwargs):
        request = args[-1]
        remote_addr = request.META.get("REMOTE_ADDR")
        user = request.META.get("USER")
        request_method = request.META.get("REQUEST_METHOD")
        path = request.META.get("PATH_INFO")
        query_string = request.META.get("QUERY_STRING")
        msg = {
            "request_time": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),  # utc time
            "remote_addr": remote_addr,
            "user": user,
            "request_method": request_method,
            "path": path,
            "query_string": query_string
        }
        logger.info(msg=msg)
        return func(*args, **kwargs)

    return wrapper


def admin_required(func):
    '''A decorator to make valid token is required to use the API being decorated'''

    def checker(*args, **kwargs):
        request = args[-1]
        try:
            authorization = request.META.get('HTTP_AUTHORIZATION')
            if authorization:
                try:
                    token_dict = jwt.decode(authorization, JWT_SECRET_KEY, algorithms=['HS256'])
                    username = token_dict.get('data').get('username')
                except Exception as e:
                    return JsonResponse(add_response(), status=status.HTTP_401_UNAUTHORIZED)
                try:
                    user = Emp.objects.get(username=username)  # query from DB
                except Emp.DoesNotExist:
                    return JsonResponse(add_response(), status=status.HTTP_401_UNAUTHORIZED)
                if not user.is_superuser:
                    return JsonResponse(add_response(), status=status.HTTP_403_FORBIDDEN)
            else:
                return JsonResponse(add_response(), status=status.HTTP_401_UNAUTHORIZED)
        except AttributeError:
            return JsonResponse(add_response(), status=status.HTTP_401_UNAUTHORIZED)
        return func(*args, **kwargs)

    return checker


def add_response(ret_list=[], count=0) -> dict:
    """
    a function to format response structure like that:
    {"count":0,
     "result":[]
    }
    :param ret_list:
    :param count:
    :return:
    """
    response_dict = {
        "count": count,
        "result": ret_list
    }
    return response_dict
