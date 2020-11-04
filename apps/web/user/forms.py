

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

class UserRole0ForPutForm(Form):

    menus = StringField("菜单集合")
