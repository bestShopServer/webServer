
import json
from wtforms.fields import StringField,IntegerField,DecimalField,SelectField
from wtforms import ValidationError
from wtforms_tornado import Form
from wtforms.validators import DataRequired, Length

class FareRuleForm(Form):

    fare_rule_id = IntegerField()
    userid = IntegerField("用户代码",validators=[DataRequired(message="请输入用户代码")])
    fare_rule_name = StringField("规则名称", validators=[DataRequired(message="请输入规则名称"), Length(min=2,max=60, message="规则名称长度为1-60")])

    fare_rule_fee_type = SelectField(
        label='计费方式',
        choices=(
            ('0', '按重计费'),
            ('1', '按件计费'),
        )
    )

    fare_rule_first_weight =IntegerField()
    fare_rule_first_fee = DecimalField()
    fare_rule_join_weight = IntegerField()
    fare_rule_join_fee = DecimalField()

    fare_rule_link_citys = StringField()

    def validate_fare_rule_link_citys(self, field):
        try:
            json.dumps(field.data)
        except Exception as e:
            print(e)
            raise ValidationError("运费规则城市关联格式有误!")

        form_obj = FareLinkCityForm(field.data)

        if not form_obj.validate():
            error_str = ""
            for field in form_obj.errors:
                error_str += "{}; ".format(form_obj.errors[field][0])
            raise ValidationError(error_str)

class FareLinkCityForm(Form):
    id = IntegerField()
    fare_rule_id = IntegerField()
    province = StringField()
    province_name = StringField()
    city = StringField()
    city_name = StringField()
    country = StringField()
    country_name = StringField()
