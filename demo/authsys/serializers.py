from rest_framework import serializers
from .models import Emp, Org


class EmpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emp
        fields = ['UUID', 'name', 'empno']
