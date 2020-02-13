# celery tasks
from __future__ import absolute_import
from celery import shared_task
from .models import Emp, Org, JWT_SECRET_KEY
from rest_framework.response import Response
from rest_framework import status
from .serializers import OrganisationSerializer, EmpSerializer
from .utils import logger_decorator, admin_required, add_response


@shared_task
def add(x, y):
    return x + y


@shared_task
def add_employee(request_data):
    try:
        org = Org.objects.filter(ID=int(request_data.get("group")[0])).first()
        user = Emp(username=request_data.get('username')[0], empno=int(request_data.get("empno")[0]))
        user.save()
        user.group.add(org)  # many-to-many relationship
        return add_response()
    except Exception as e:
        return add_response([{'error':str(e)}])
