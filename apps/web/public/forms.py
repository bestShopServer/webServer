

from wtforms.fields import StringField,IntegerField
from wtforms import ValidationError
from wtforms_tornado import Form
from wtforms.validators import DataRequired, Length


class AttachMentGroupForm(Form):

    id = IntegerField()
    userid = IntegerField("用户代码",validators=[DataRequired(message="请输入用户代码")])
    name = StringField("分组名称", validators=[DataRequired(message="请输入分组名称"), Length(min=2,max=30, message="分组名称长度为2-30")])
    type = StringField("素材类型", validators=[DataRequired(message="请输入素材类型")])

    def validate_type(self,field):
        if field.data not in ('image', 'video'):
            raise ValidationError("类型超出范围(图片,视频)")

class AttachMentForm(Form):

    id = IntegerField()
    grouid = IntegerField()
    userid = IntegerField("用户代码", validators=[DataRequired(message="请输入用户代码")])
    name = StringField("素材名称", validators=[DataRequired(message="请输入素材名称"), Length(min=2,max=60, message="素材名称长度为2-60")])
    type = StringField("素材类型", validators=[DataRequired(message="请输入素材类型")])
    url = StringField("素材链接", validators=[DataRequired(message="请输入素材链接")])

    def validate_type(self,field):
        if field.data not in ('image', 'video'):
            raise ValidationError("类型超出范围(图片,视频)")