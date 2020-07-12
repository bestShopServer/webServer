
import json
from wtforms.fields import StringField,IntegerField,DecimalField
from wtforms import ValidationError
from wtforms_tornado import Form
from wtforms.validators import DataRequired, Length
from apps.web.goods.customdict import GoodsCateGoryStyleTypecode

class GoodsCateGoryStyleForm(Form):

    id = IntegerField()
    userid = IntegerField("用户代码",validators=[DataRequired(message="请输入用户代码")])
    typecode = StringField("分类样式代码", validators=[DataRequired(message="请输入分类样式代码"), Length(min=2,max=10, message="分类样式代码长度为1-20")])
    type = IntegerField("几级分类", validators=[DataRequired(message="请输入几级分类")])

    def validate_type(self,field):
        if field.data not in (1,2,3):
            raise ValidationError("几级分类超出范围(1,2,3)")

    def validate_typecode(self,field):
        if field.data not in [ item[0] for item in GoodsCateGoryStyleTypecode().data ]:
            raise ValidationError("分类样式代码超出范围")

class GoodsCateGoryForm(Form):

    gdcgid = IntegerField()
    gdcglastid = IntegerField(default=0)
    level = IntegerField()
    sort = IntegerField(default=1)
    status = StringField("状态", default='0')
    userid = IntegerField("用户代码", validators=[DataRequired(message="请输入用户代码")])
    gdcgname = StringField("分类名称", validators=[DataRequired(message="请输入分类名称"), Length(min=2,max=10, message="分类名称长度为2-10")])
    url = StringField("分类图标")
    url_big = StringField("分类大图")
    url_poster = StringField("分类广告图")

class SkuGroupForm(Form):

    group_id = IntegerField()
    group_name = StringField("分组名称", validators=[DataRequired(message="请输入分组名称"), Length(min=2,max=10, message="分组名称长度为2-10")])
    userid = IntegerField("用户代码", validators=[DataRequired(message="请输入用户代码")])

class SkuSpecValueForm(Form):

    spec_id = IntegerField()
    group_id = IntegerField("分组ID",validators=[DataRequired(message="请输入分组ID")])
    spec_value =StringField("值名称", validators=[DataRequired(message="请输入值名称"), Length(min=2,max=10, message="值名称长度为2-20")])
    userid = IntegerField("用户代码", validators=[DataRequired(message="请输入用户代码")])

class GoodsForm(Form):

    gdid = IntegerField()
    userid = IntegerField("用户代码", validators=[DataRequired(message="请输入用户代码")])
    gd_name = StringField("商品名称", validators=[DataRequired(message="请输入商品名称"), Length(min=2,max=60, message="商品名称长度为2-60")])
    gd_banners = StringField("商品轮播",default='[]')
    gd_status = StringField("上下架状态", default='1')
    gd_sort = IntegerField(default=1)
    gd_show_price = DecimalField("商品售价",default=0.0)
    gd_mark_price = DecimalField("商品原价",default=0.0)
    gd_unit = StringField("单位", validators=[DataRequired(message="请输入单位"), Length(min=1,max=10, message="单位长度为1-10")])
    gd_cost_price = DecimalField("成本价",default=0.0)
    gd_stock_tot = IntegerField(default=0)
    gd_stock_show = StringField("是否显示库存", default='0')
    gd_specs_name_default = StringField("默认规格名",default="默认")
    gd_specs_name_default_flag = StringField("是否使用默认规格",default="0")
    gd_item_no = StringField("货号")
    gd_weight = IntegerField("重量")
    gd_sku_link = StringField('商品SKU关联',default='[]')

    gd_sell_number = IntegerField("已出售数量",default=0)
    gd_fare_mould_id = IntegerField("运费模板ID",default=0)
    gd_limit_number_by_goods = IntegerField("限购数量(商品)",default=-1)
    gd_limit_number_by_order = IntegerField("限购数量(订单)",default=-1)

    attribute = StringField()

    gd_include_fare1 = IntegerField("单品满件包邮(件)",default=0)
    gd_include_fare2 = DecimalField("单品满额包邮(元)",default=0.0)
    gd_allow_area_flag = StringField("是否允许区域购买", default='1')
    gd_allow_area = StringField("购买区域集合",default='[]')

    gd_share_title = StringField("分享标题",default="")
    gd_share_image = StringField("分享图片",default="")

    gd_link_type = StringField("商品关联分类集合",default='[]')


    def validate_gd_banners(self,field):
        try:
            json.dumps(field.data)

            if field.data[0][0] != 'image':
                raise ValidationError("第一张必须是图片!")
        except Exception:
            raise ValidationError("商品轮播格式有误!")

    def validate_gd_link_type(self,field):
        try:
            json.dumps(field.data)
        except Exception:
            raise ValidationError("商品关联分类集合格式有误!")
