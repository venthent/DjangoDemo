from rest_framework import serializers
from .models import Emp, Org,EmployeeType


# class EmpSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Emp
#         fields = ['UUID', 'name', 'empno']


class EmpSerializer(serializers.Serializer):
    UUID = serializers.UUIDField(read_only=True)
    username = serializers.CharField(required=True)
    empno=serializers.IntegerField()
    # group = serializers.CharField(source='group.all')

    # def create(self, validated_data):
    #     return User.objects.create(**validated_data)
#
#
# from enum import Enum
#
#
# class EmployeeType(Enum):
#     DEV = '开发'
#     OPS = '运维'
#     PRD = '产品'
#     TEST = '测试'


class OrganisationSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False, read_only=True)
    name = serializers.CharField(required=True)
    type = serializers.ChoiceField(required=True, choices=[(tag.name, tag.value) for tag in EmployeeType])

    def create(self, validated_data):
        return Org.objects.create(**validated_data)

    def update(self, instance, validated_data):
        pass
