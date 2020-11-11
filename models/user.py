

from peewee import *
from models.base import BaseModel

from models.choices import *

class User(BaseModel):

    """
    用户表
    """

    userid = BigAutoField(verbose_name="用户ID")

    role_type=CharField(verbose_name="类别",choices=ROLE_TYPES_CHOICES)

    status = CharField(max_length=1,default='0',verbose_name="状态",choices=USER_STATUS_CHOICES)

    name = CharField(max_length=60, verbose_name="名称", default='')
    pic = CharField(max_length=255, verbose_name="头像地址", default='')
    address = CharField(max_length=255, verbose_name="地址", default='')
    sex = CharField(max_length=1, verbose_name="性别", default='0',choices=USER_SEX_CHOICES)

    memo = CharField(max_length=255,verbose_name="备注",default="")

    points = DecimalField(max_digits=18, decimal_places=6, default=0.000, verbose_name="积分")
    balance = DecimalField(max_digits=18, decimal_places=6, default=0.000, verbose_name="余额")

    merchant_id = BigIntegerField(verbose_name="商户ID",default=0)

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

    is_password = CharField(max_length=1,verbose_name="是否可以密码登录",choices=DEFAULT_CHOICES,default="0")

    class Meta:
        db_table = 'userauth'


class UserRole(BaseModel):

    """
    用户角色信息表
    """

    role_id = BigAutoField(primary_key=True)
    role_type = CharField(max_length=1,default='0',verbose_name="角色类型",choices=ROLE_TYPES_CHOICES)

    role_name = CharField(max_length=60,verbose_name="角色名称",default='')

    sort = IntegerField(verbose_name="排序",default=0)
    status = CharField(max_length=1,verbose_name="状态",choices=STATUS_CHOICES,default='0')

    menus = TextField(verbose_name="菜单集合",default="[]")
    merchant_id = BigIntegerField(verbose_name="商户ID")

    class Meta:
        db_table = 'role'

class UserLinkRole(BaseModel):

    """
    用户角色关联表
    """

    id = BigAutoField(primary_key=True)
    userid = BigIntegerField(verbose_name="用户ID")
    role_id = BigIntegerField(verbose_name="角色ID")

    class Meta:
        db_table = 'userlinkrole'


class Branch(BaseModel):

    """
    公司部门表
    """

    branch_id = BigAutoField(primary_key=True)

    parent_branch_id = BigIntegerField(default=0)
    branch_name = CharField(max_length=60,verbose_name="部门名称",default='')

    super_man_name = CharField(max_length=60,verbose_name="负责人",default='')
    super_man_phone = CharField(max_length=60,verbose_name="联系电话",default='')
    super_man_email = CharField(max_length=60,verbose_name="邮箱",default='')

    status = CharField(max_length=1, verbose_name="状态", choices=STATUS_CHOICES,default='0')
    merchant_id = BigIntegerField(verbose_name="商户ID")

    sort = IntegerField(default=0,verbose_name="排序")

    class Meta:
        db_table = 'branch'

class UserLinkBranch(BaseModel):

    """
    用户部门关联表
    """

    id = BigAutoField(primary_key=True)
    userid = BigIntegerField(verbose_name="用户ID")
    branch_id = BigIntegerField(verbose_name="部门ID")

    class Meta:
        db_table = 'userlinkbranch'

class MenuLinkMerchantSetting(BaseModel):
    """
    租户权限范围授权配置表
    """

    id = BigAutoField(primary_key=True)
    default = CharField(max_length=1,verbose_name="是否默认",default='1',choices=DEFAULT_CHOICES)
    name = CharField(max_length=60,verbose_name="权限名称",default="")
    status = CharField(max_length=1, verbose_name="状态", choices=STATUS_CHOICES,default='0')
    memo = CharField(max_length=255,verbose_name="描述",default="")
    menus = TextField(verbose_name="菜单集合",default="[]")

    class Meta:
        db_table = 'menulinkmerchantsetting'


class Merchant(BaseModel):
    """
    商户表
    """
    merchant_id = BigAutoField(verbose_name="商户ID")
    merchant_name = CharField(max_length=60, verbose_name="商户名称", default='')

    sort = IntegerField(verbose_name="排序", default=0)
    memo = CharField(max_length=255,verbose_name="备注",default="")

    status = CharField(max_length=1, verbose_name="状态", choices=STATUS_CHOICES,default='0')

    expire_time = BigIntegerField(default=0,verbose_name="到期时间")

    userid = BigIntegerField(verbose_name="第一个用户",default=0)

    class Meta:
        db_table = 'merchant'

class UserLinkMerchant(BaseModel):

    """
    用户商户关联表
    """

    id = BigAutoField(primary_key=True)
    userid = BigIntegerField(verbose_name="用户ID")
    merchant_id = BigIntegerField(verbose_name="商户ID")

    class Meta:
        db_table = 'userlinkmerchant'


