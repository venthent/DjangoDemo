from django.shortcuts import render
from rest_framework import mixins
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import JsonResponse
import jwt

from .models import Emp, Org, User,JWT_SECRET_KEY
from .serializers import EmpSerializer
# from ..demo.settings import JWT_SECRET_KEY


def admin_required(func):
    '''Decorator to make valid token is required to use the API being decorated'''

    def checker(*args, **kwargs):
        request = args[-1]
        try:
            authorization = request.META.get('HTTP_AUTHORIZATION')
            if authorization:
                username=None
                try:
                    token_dict=jwt.decode(authorization,JWT_SECRET_KEY,algorithms=['HS256'])
                    username=token_dict.get('data').get('username')
                except Exception as e:
                    print(e)
                try:
                    user=User.objects.get(username=username)
                except User.DoesNotExist:
                    return JsonResponse({},status=status.HTTP_401_UNAUTHORIZED)
                if not user.is_superuser:
                    return JsonResponse({},status=status.HTTP_403_FORBIDDEN)
            else:
                return JsonResponse({},status=status.HTTP_401_UNAUTHORIZED)
        except AttributeError:
            return JsonResponse({"1":"error"},status=status.HTTP_401_UNAUTHORIZED)
        return func(*args, **kwargs)

    return checker


class EmployeesList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Emp.objects.all()
    serializer_class = EmpSerializer

    @admin_required
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class AuthView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            username = request.data.get('username')
            passwd = request.data.get('password')
            # print("heder:",request.META.get('HTTP_AUTHORIZATION'))
            obj = User.objects.filter(username=username).first()
            passwd_is_correct = obj.check_password(passwd)
            if passwd_is_correct:
                return JsonResponse({'token': obj.token})
        except Exception as e:
            print(e)
        return JsonResponse({"hello": "world"})

# Create your views here.
