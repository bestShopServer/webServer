
import json
from wtforms.fields import StringField,IntegerField,DecimalField,SelectField
from wtforms import ValidationError
from wtforms_tornado import Form
from wtforms.validators import DataRequired, Length

class ShopPageForm(Form):

    id = IntegerField()
    merchant_id = IntegerField("商户ID",validators=[DataRequired(message="请输入商户ID")])
    title = StringField("标题", validators=[DataRequired(message="请输入标题"), Length(min=2,max=60, message="标题长度为2-60")])
    type = StringField(default='1')

    time_publish_flag = SelectField(
        label='是否定时发布',
        choices=(
            ('0', '是'),
            ('1', '否'),
        )
    )

    time_publish = IntegerField()
    html_data = StringField()

class ShopConfigForm(Form):

    id = IntegerField()
    merchant_id = IntegerField("商户ID",validators=[DataRequired(message="请输入商户ID")])
    navigation_data = StringField()