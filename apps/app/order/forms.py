
import json
from wtforms.fields import StringField,IntegerField,DecimalField,SelectField
from wtforms import ValidationError
from wtforms_tornado import Form
from wtforms.validators import DataRequired, Length

class AddressForm(Form):

    id = IntegerField()
    userid = IntegerField("用户代码",validators=[DataRequired(message="请输入用户代码")])
    name = StringField("收货名称", validators=[DataRequired(message="请输入收货名称"), Length(min=2,max=20, message="收货名称长度2-20")])
    mobile = IntegerField("收货手机号", validators=[DataRequired(message="请输入收货手机号")])

    merchant_id = IntegerField("商户ID")

    province_code = StringField()
    province_name = StringField()

    city_code = StringField()
    city_name = StringField()

    county_code = StringField()
    county_name = StringField()

    address_detail = StringField("详细地址",validators=[DataRequired(message="请输入详细地址")])
    address_default = SelectField(
        label='是否默认地址',
        choices=(
            ('0', '是'),
            ('1', '否'),
        )
    )
