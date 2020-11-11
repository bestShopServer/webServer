
import re

from wtforms.fields import StringField,IntegerField,SelectField,FormField
from wtforms import ValidationError
from wtforms_tornado import Form
from wtforms.validators import DataRequired, Length,Email

from models.choices import *



class BranchFrom(Form):

    branch_id = IntegerField()

    parent_branch_id = IntegerField()
    branch_name = StringField("部门名称")

    super_man_name = StringField("负责人")
    super_man_phone = StringField("联系电话")
    super_man_email = StringField("邮箱")

    status = StringField("状态")
    sort = IntegerField()

class UserRole0Form(Form):

    role_id = IntegerField()
    role_type = StringField("角色分类",default='0')

    role_name = StringField("角色名称", validators=[DataRequired(message="角色名称")])

    sort = IntegerField()
    status = StringField("状态",default="0")

class UserRole0ForPutForm(Form):

    role_id = IntegerField()
    role_type = StringField()

    role_name = StringField()

    sort = IntegerField()
    status = StringField()
    menus = StringField()

class MenuLinkMerchantSettingPostForm(Form):

    # id = IntegerField()
    default = SelectField(
        label='是否默认',
        choices=DEFAULT_CHOICES,
        default="1"
    )
    name = StringField("权限名称",validators=[DataRequired(message="请输入权限名称!")])
    status = SelectField(
        label='状态',
        choices=STATUS_CHOICES,
        default="0"
    )
    memo = StringField("权限备注")
    menus = StringField("菜单集合",default="[]")

class MenuLinkMerchantSettingPutForm(Form):

    id = IntegerField()
    default = StringField()
    name = StringField()
    status = StringField()
    memo = StringField()
    menus = StringField()

class MerchantPostForm(Form):

    merchant_name = StringField("租户名称",validators=[DataRequired(message="请输入租户名称!")])
    sort = IntegerField("排序",default=0)
    memo = StringField("租户描述")
    status = SelectField(
        label='状态',
        choices=STATUS_CHOICES,
        default="0"
    )
    expire_time = IntegerField("到期时间",default=0)

class MerchantPutForm(Form):

    merchant_id = IntegerField()
    merchant_name = StringField()
    sort = IntegerField()
    memo = StringField()
    status = StringField()
    expire_time = IntegerField()

    account = StringField()
    password = StringField()

class User0PostForm(Form):

    role_type=StringField(default="0")
    name = StringField("用户名称",validators=[DataRequired(message="请输入用户名称!")])
    login_name = StringField("登录名称", validators=[DataRequired(message="请输入登录名称!")])

    mobile = StringField("手机号", validators=[DataRequired(message="请输入手机号!")])
    email = StringField("邮箱", validators=[DataRequired(message="请输入邮箱")])
    password = StringField("密码", validators=[DataRequired(message="请输入密码!")])
    sex = SelectField(
        label='性别',
        choices=USER_SEX_CHOICES,
        default="0"
    )

    memo = StringField()
    branchs = StringField("部门",default='[]')
    roles = StringField("角色",default='[]')
    status = SelectField(
        label='状态',
        choices=STATUS_CHOICES,
        default="0"
    )

    def validate_mobile(self,field):

        if field.data:
            t=re.compile('^(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}$')
            if not re.search(t, field.data):
                raise ValidationError("手机号非法!")

    def validate_email(self,field):

        if field.data:
            t=r'^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$'
            if not re.match(t, field.data):
                raise ValidationError("邮箱非法!")

class User0PutForm(Form):

    userid = IntegerField()
    name = StringField("用户名称")
    login_name = StringField("登录名称")

    mobile = StringField("手机号")
    email = StringField("邮箱")
    password = StringField("密码")
    sex = StringField()
    memo = StringField()
    branchs = StringField("部门")
    roles = StringField("角色")
    status = StringField()

    def validate_mobile(self,field):

        if field.data:
            t=re.compile('^(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}$')
            if not re.search(t, field.data):
                raise ValidationError("手机号非法!")

    def validate_email(self,field):

        if field.data:
            t=r'^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$'
            if not re.match(t, field.data):
                raise ValidationError("邮箱非法!")