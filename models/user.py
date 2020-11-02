

from peewee import *
from models.base import BaseModel

from models.choices import *

class User(BaseModel):

    """
    用户表
    """

    userid = BigAutoField(verbose_name="用户ID")
    role_code=CharField(verbose_name="角色代码",max_length=6)
    status = CharField(max_length=1,default='0',verbose_name="状态",choices=USER_STATUS_CHOICES)

    name = CharField(max_length=60, verbose_name="名称", default='')
    pic = CharField(max_length=255, verbose_name="头像地址", default='')
    address = CharField(max_length=255, verbose_name="地址", default='')
    sex = CharField(max_length=10, verbose_name="性别", default='')

    points = DecimalField(max_digits=18, decimal_places=6, default=0.000, verbose_name="积分")
    balance = DecimalField(max_digits=18, decimal_places=6, default=0.000, verbose_name="余额")

    class Meta:
        db_table = 'user'

class UserAuth(BaseModel):

    """
    用户授权登录表
    """

    id = BigAutoField()
    userid = BigIntegerField(verbose_name="用户代码")

    type = CharField(max_length=1,verbose_name="登录类别",choices=LOGIN_TYPES_CHOICES,default='0')

    account = CharField(max_length=60,verbose_name="账号",default="")
    ticket = CharField(max_length=60,verbose_name="令牌/密码",default="e10adc3949ba59abbe56e057f20f883e")


    class Meta:
        db_table = 'userauth'

class UserRole(BaseModel):

    """
    用户角色信息表
    """

    id = BigAutoField(primary_key=True)
    role_code = CharField(max_length=6,verbose_name="角色代码",default='')
    role_type = CharField(max_length=1,default='0',verbose_name="角色类型",choices=ROLE_TYPES_CHOICES)

    role_name = CharField(max_length=60,verbose_name="角色名称",default='')
    role_app_type = CharField(max_length=1,verbose_name="端",choices=APP_TYPES_CHOICES)

    """
    角色代码:
        100000 - 超级管理员
        200000 - 商户超级管理员
        300000 - 用户
    """

    class Meta:
        db_table = 'role'
