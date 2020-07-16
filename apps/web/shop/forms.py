
import json
from wtforms.fields import StringField,IntegerField,DecimalField,SelectField
from wtforms import ValidationError
from wtforms_tornado import Form
from wtforms.validators import DataRequired, Length

class ShopPageForm(Form):

    id = IntegerField()
    userid = IntegerField("用户代码",validators=[DataRequired(message="请输入用户代码")])
    title = StringField("标题", validators=[DataRequired(message="请输入标题"), Length(min=2,max=60, message="标题长度为2-60")])
    type = StringField(default='9')

    time_publish_flag = SelectField(
        label='是否定时发布',
        choices=(
            ('0', '是'),
            ('1', '否'),
        )
    )

    time_publish = StringField()
    html_data = StringField()

class ShopPageUpdateForm(Form):

    id = IntegerField()
    userid = IntegerField("用户代码",validators=[DataRequired(message="请输入用户代码")])
    title = StringField()
    type = StringField()
    time_publish_flag = StringField()
    time_publish = StringField()
    html_data = StringField()

class ShopConfigForm(Form):

    id = IntegerField()
    userid = IntegerField("用户代码",validators=[DataRequired(message="请输入用户代码")])
    navigation_data = StringField()