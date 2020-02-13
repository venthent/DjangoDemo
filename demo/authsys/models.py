import uuid
import os
import datetime
from enum import Enum

from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, PermissionsMixin, BaseUserManager, Group
import jwt

# from ..demo.settings import JWT_SECRET_KEY, JWT_EXPIRE_TIME

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY") or "ThisIsASecretKEY"
JWT_EXPIRE_TIME = 60  # minutes


class EmployeeType(Enum):
    DEV = '开发'
    OPS = '运维'
    PRD = '产品'
    TEST = '测试'


class UserManger(BaseUserManager):
    def _create_user(self, username, password, **kwargs):

        if not username:
            raise ValueError('请输入用户名！')
        if not password:
            raise ValueError('请输入密码！')
        user = self.model(username=username, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, username, password, **kwargs):

        kwargs['is_superuser'] = False
        return self._create_user(username, password, **kwargs)

    # 创建超级用户
    def create_superuser(self, username, password, **kwargs):

        kwargs['is_superuser'] = True
        return self._create_user(username, password, **kwargs)


class Emp(AbstractBaseUser, PermissionsMixin):
    UUID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    empno = models.BigIntegerField(unique=True, db_index=True, max_length=50, null=False, help_text="employees' number")
    username = models.CharField(max_length=100, unique=False)
    group = models.ManyToManyField('Org')
    email = models.EmailField(unique=False)
    is_active = models.BooleanField(default=True)  # 是否是可用的
    is_staff = models.BooleanField(default=False)  # 是否是员工
    date_joined = models.DateTimeField(auto_now_add=True)  # 加入时间

    USERNAME_FIELD = 'empno'  # 作为唯一认证标识， 如果不重写User模型则默认username
    REQUIRED_FIELDS = ['username']  # 设置此属性会提示 username,telephone,password
    EMAIL_FIELD = 'email'  # 给指定用户发送邮件

    objects = UserManger()

    def __str__(self):
        return self.username

    def get_full_name(self):  # 必须定义。 long格式的用户标识。
        return self.username

    def get_short_name(self):  # 必须定义。 short格式的用户标识。
        return self.username

    @property
    def token(self):
        data = {'username': self.username}
        return self._generate_token(data)

    def _generate_token(self, data: dict):
        """
        create a JWT token
        :return: str
        """
        token = jwt.encode({
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=JWT_EXPIRE_TIME),
            'iat': datetime.datetime.utcnow(),
            'data': data
        }, key=JWT_SECRET_KEY)
        return token.decode()


class Org(models.Model):
    """
    Organisation model
    """
    ID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True, db_index=True)
    type = models.CharField(max_length=50, choices=[(tag.name, tag.value) for tag in EmployeeType])

# class Emp(models.Model):
#     """
#     Employee model
#     """
#     UUID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     name = models.CharField(max_length=50, null=False, default='')
#     empno = models.BigIntegerField(unique=True, db_index=True, max_length=50, null=False, help_text="employees' number")

# class Meta:
#     ordering = ['name']

