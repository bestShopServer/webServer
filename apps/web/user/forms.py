

from wtforms.fields import StringField,IntegerField,SelectField
from wtforms import ValidationError
from wtforms_tornado import Form
from wtforms.validators import DataRequired, Length

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

class UserRole0ForPutForm(UserRole0Form):

    menus = StringField("菜单集合")

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