from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import JsonResponse

from .models import Emp, Org, JWT_SECRET_KEY
from .serializers import OrganisationSerializer, EmpSerializer
from .utils import logger_decorator, admin_required, add_response


#
# class EmployeesList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = Emp.objects.all()
#     serializer_class = EmpSerializer
#
#     @admin_required
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


class AuthView(APIView):
    """An api for admin login"""

    def post(self, request, *args, **kwargs):
        try:
            username = request.data.get('username')
            passwd = request.data.get('password')
            obj = Emp.objects.filter(username=username).first()
            passwd_is_correct = obj.check_password(passwd)  # check password
            if passwd_is_correct:
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
    def post(self, request, *args, **kwargs):
        try:
            org = Org.objects.filter(ID=request.data.get("group")).first()
            user = Emp(username=request.data.get('username'), empno=request.data.get("empno"))
            user.save()
            user.group.add(org)  # many-to-many relationship
            return JsonResponse(add_response())
        except Exception as e:
            return JsonResponse(add_response(), status=status.HTTP_400_BAD_REQUEST)

        # serializer = UserSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrganisationView(APIView):
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
