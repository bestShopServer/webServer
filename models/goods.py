
from peewee import *
from models.base import BaseModel

class GoodsCateGoryStyle(BaseModel):
    """
    商品分类样式表 1-3级
    """
    id = BigAutoField(primary_key=True)
    merchant_id = BigIntegerField(verbose_name="商户ID")
    typecode = CharField(max_length=20,verbose_name="分类样式代码")
    type = IntegerField(verbose_name="几级分类",default=1)

    class Meta:
        db_table = 'goodscategorystyle'

class GoodsCateGory(BaseModel):

    """
    商品分类表: 支持无限级扩展  业务场景限制目前最多支持3层
    """
    gdcgid = BigAutoField(primary_key=True)
    gdcgname = CharField(max_length=120, default="",verbose_name="分类名称",null=True)

    merchant_id = BigIntegerField(verbose_name="商户ID")

    gdcglastid = CharField(max_length=10,default=0,verbose_name="上级代码",null=True)

    level = IntegerField(verbose_name="第几层",default=1,null=True)
    sort = IntegerField(verbose_name="排序",default=0,null=True)
    status = CharField(max_length=1, default="1",verbose_name="是否上架,0-是,1-否",null=True)
    url = CharField(max_length=255,verbose_name="分类图标",default="")
    url_big = CharField(max_length=255,verbose_name="分类大图",default="")
    url_poster = CharField(max_length=255,verbose_name="分类广告图",default="")

    class Meta:
        db_table = 'goodscategory'


class Goods(BaseModel):

    """
    商品表基础信息表gd_sku_link
    """

    """
    商品设置
    """
    gdid = BigAutoField(primary_key=True,verbose_name="商品ID")

    merchant_id = BigIntegerField(verbose_name="商户ID")

    gd_name = CharField(max_length=120, verbose_name="商品名称", default='', null=True)
    gd_banners = CharField(max_length=2048, verbose_name="商品轮播,支持图片和视频['image','url'],['video','url']", default='[]')
    gd_status = CharField(verbose_name="商品状态,0-上架(销售中),1-下架,2-已售罄",default='1',max_length=1)
    gd_sort = IntegerField(verbose_name="排序", default=0)


    """
    价格库存
    """
    gd_show_price = DecimalField(max_digits=18,decimal_places=6,default=0.000,verbose_name="商品显示价格(售价)")
    gd_mark_price = DecimalField(max_digits=18,decimal_places=6,default=0.000,verbose_name="商品划线价格(原价)")
    gd_unit = CharField(max_length=20,verbose_name="单位",default="件")
    gd_cost_price = DecimalField(max_digits=18,decimal_places=6,default=0.000,verbose_name="成本价")

    gd_stock_tot = IntegerField(verbose_name="总库存",default=0)
    gd_stock_show = CharField(max_length=1,verbose_name="是否显示库存! 0-显示,1-不显示",default='0')
    gd_specs_name_default_flag = CharField(max_length=1,verbose_name="是否使用默认规格! 0-是,1-否",default='0')
    gd_specs_name_default = CharField(max_length=60,verbose_name="默认规格名",default='默认')

    gd_item_no = CharField(max_length=60,verbose_name="商品货号",default="")
    gd_weight = IntegerField(verbose_name="商品重量(单位克)",default=0)

    gd_sku_links = CharField(max_length=2048,verbose_name='商品sku关联ID集合 {"group_id":1,"spec_id":1}',default="[]")

    gd_sell_actual_number = IntegerField(verbose_name="实际出售数量",default=0)

    # gd_stock_reduce_type = CharField(max_length=1,verbose_name="库存扣减方式 0-加入购物车扣减,1-付款扣减,2-加入购物车扣减,一定时间系统自动清除购物车返还给库存!",default="")
    # gd_stock_valid_time = IntegerField(verbose_name="库存扣减未支付返回库存,当库存扣减方式为2时，此值有效,单位是分钟",default=0)

    """
    购买设置
    """
    gd_sell_number = IntegerField(verbose_name="已出售量",default=0)

    gd_sell_tot_number = IntegerField(verbose_name="总销售量",default=0)
    gd_fare_mould_id = BigIntegerField(verbose_name="运费模板ID",default=0)
    gd_limit_number_by_goods = IntegerField(verbose_name="限购数量(商品)",default=-1)
    gd_limit_number_by_order = IntegerField(verbose_name="限购数量(订单)",default=-1)

    gd_include_fare1 = IntegerField(verbose_name="单品满件包邮(件)  0不支持包邮",default=0)
    gd_include_fare2 = DecimalField(max_digits=18,decimal_places=6,verbose_name="单品满额包邮(元) 0.0不支持包邮,",default=0.0)
    gd_allow_area_flag = CharField(max_length=1,verbose_name="是否允许区域购买 0-是,1-否",default="1")


    """
    分享图片
    """
    gd_share_title = CharField(max_length=60,verbose_name="分享标题",default="")
    gd_share_image = CharField(max_length=255,verbose_name="分享图片",default="")

    attribute = TextField(default="")

    gd_link_shoppage = BigIntegerField(default=0)
    # gdotherinfo = CharField(max_length=512,default="{}",verbose_name="""
    #                     "uptime" -> 上架时间
    #                     "willsell" -> 预售
    #                         "flag" -> 0 不预售 1 预售
    #                         "type" -> 预售方式 0-按日期,1-付款成功后多少天
    #                         "value" -> 如果预售 那么此处就是指定的日期或天数
    #                     "limitsell" -> 限够(限制每人可购买数量)
    #                         "flag" -> 是否限购 0-不限购,1-限购
    #                         "type" -> 限购方式 0-终身限购,1-按周期限购
    #                         "value" ->限购数量/周期限购(年->Y,月->M,周->W,如果是按每年100件那么值就是Y,100)
    #                     "sharememo" -> 分享描述
    #                     "selltype" -> 商品卖点
    #                 """)

    gd_link_type = None
    gd_allow_area = None

    class Meta:
        db_table = 'goods'


class GoodsLinkCity(BaseModel):
    """
    商品城市区域关联表
    """

    id = BigAutoField(primary_key=True,verbose_name="关联ID")
    merchant_id = BigIntegerField(verbose_name="商户ID")
    gdid = BigIntegerField(verbose_name="商品ID")
    citycode = CharField(max_length=30,verbose_name="城市代码")
    cityname = CharField(max_length=60,verbose_name="城市名称")

    class Meta:
        db_table = 'goodslinkcity'

class GoodsLinkCateGory(BaseModel):

    """
    商品分类表关联
    """

    id = BigAutoField(primary_key=True,verbose_name="关联ID")
    merchant_id = BigIntegerField(verbose_name="商户ID")
    gdid = BigIntegerField(verbose_name="商品ID")
    gdcgid = BigIntegerField(verbose_name="分类ID")

    gdcgname = None

    class Meta:
        db_table = 'goodslinkcategory'


class GoodsLinkSku(BaseModel):

    id = BigAutoField(primary_key=True)
    gdid = BigIntegerField(verbose_name="商品ID", null=True)
    merchant_id = BigIntegerField(verbose_name="商户ID")
    skus = CharField(max_length=1024,verbose_name='sku集合 {"group_id":1,"spec_id":2}',default=[])

    image = CharField(verbose_name="图片",max_length=255,default="")
    price = DecimalField(max_digits=18,decimal_places=6,default=0.000,verbose_name="价格")
    stock = IntegerField(verbose_name="库存",default=0)
    item_no = CharField(max_length=60,verbose_name="商品货号",default="")
    weight = IntegerField(verbose_name="商品重量(单位克)",default=0)
    cost_price = DecimalField(max_digits=18,decimal_places=6,default=0.000,verbose_name="成本价")
    number = IntegerField(verbose_name="销量",default=0)
    sort = IntegerField(verbose_name="排序",default=0)

    class Meta:
        db_table = 'goodslinksku'


class SkuGroup(BaseModel):

    """
    sku组
    """

    group_id = BigAutoField(primary_key=True)
    group_name = CharField(verbose_name="sku组名称",default='',max_length=60)
    merchant_id = BigIntegerField(verbose_name="商户ID")

    spec_values=None

    class Meta:
        db_table = 'skugroup'

class SkuSpecValue(BaseModel):

    """
    sku值
    """

    spec_id = BigAutoField(primary_key=True)

    group_id = BigIntegerField(verbose_name="sku组名称", default=0)
    spec_value = CharField(verbose_name="sku值名称",default="",max_length=60)
    merchant_id = BigIntegerField(verbose_name="商户ID")

    class Meta:
        db_table = 'skuspecvalue'
