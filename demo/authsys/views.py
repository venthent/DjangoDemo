from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import JsonResponse

from .models import Emp, Org, JWT_SECRET_KEY
from .serializers import OrganisationSerializer, EmpSerializer
from .utils import logger_decorator, admin_required, add_response
from . import tasks


class AuthView(APIView):
    """An api for admin login"""

    def post(self, request, *args, **kwargs):
        try:
            username = request.data.get('username')
            passwd = request.data.get('password')
            obj = Emp.objects.filter(username=username).first()
            passwd_is_correct = obj.check_password(passwd)  # check password
            if passwd_is_correct and obj.is_superuser:
                return JsonResponse(add_response([{"token": obj.token}], 1))
        except Exception as e:
            return JsonResponse(add_response(), status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse(add_response(), status=status.HTTP_400_BAD_REQUEST)


class EmployeeView(APIView):
    """Apis for querying or adding employees"""

    # get all the employees
    @logger_decorator
    @admin_required
    def get(self, request, *args, **kwargs):
        user = Emp.objects.filter(is_superuser=0).all()
        ret = []
        serializer = EmpSerializer(user, many=True)

        for item in serializer.data:  # this is a list
            ret.append(dict(item))  # OrderDict ->dict
        return JsonResponse(add_response(ret, count=len(serializer.data)))

    # add new employees
    @admin_required
    def post(self, request, *args, **kwargs):
        res = tasks.add_employee.delay(dict(request.data))
        # TODO:read result from DB
        return JsonResponse(add_response({}))


class OrganisationView(APIView):
    """Apis for querying or organizations"""

    def get(self, request, *args, **kwargs):
        org = Org.objects.all()

        ser = OrganisationSerializer(org, many=True)
        return Response(ser.data)

    def post(self, request, *args, **kwargs):
        serializer = OrganisationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
