

from wtforms.fields import StringField,IntegerField,SelectField
from wtforms import ValidationError
from wtforms_tornado import Form
from wtforms.validators import DataRequired, Length

from models.choices import *


class AttachMentGroupForm(Form):

    id = IntegerField()
    merchant_id = IntegerField("商户ID",validators=[DataRequired(message="请输入商户ID")])
    name = StringField("分组名称", validators=[DataRequired(message="请输入分组名称"), Length(min=2,max=30, message="分组名称长度为2-30")])
    type = StringField("素材类型", validators=[DataRequired(message="请输入素材类型")])

    def validate_type(self,field):
        if field.data not in ('image', 'video'):
            raise ValidationError("类型超出范围(图片,视频)")

class AttachMentForm(Form):

    id = IntegerField()
    grouid = IntegerField()
    merchant_id = IntegerField("商户ID",validators=[DataRequired(message="请输入商户ID")])
    name = StringField("素材名称", validators=[DataRequired(message="请输入素材名称"), Length(min=2,max=60, message="素材名称长度为2-60")])
    type = StringField("素材类型", validators=[DataRequired(message="请输入素材类型")])
    url = StringField("素材链接", validators=[DataRequired(message="请输入素材链接")])

    def validate_type(self,field):
        if field.data not in ('image', 'video'):
            raise ValidationError("类型超出范围(图片,视频)")

class MenuForm(Form):

    id = IntegerField()
    parent_id = IntegerField()
    title = StringField("标题", validators=[DataRequired(message="请输入标题")])
    type = SelectField(
        label='菜单类型',
        choices=MENU_TYPES_CHOICES
    )
    pic = StringField("图片", validators=[DataRequired(message="请传入图片")])
    sort = IntegerField()
    component = StringField("组件", validators=[DataRequired(message="请输入组件")])
    component_name = StringField("组件名称", validators=[DataRequired(message="请输入组件名称")])
    path = StringField("路由地址", validators=[DataRequired(message="请输入路由地址")])
    keep = SelectField(
        label='路由地址',
        choices=KEEP_CHOICES
    )