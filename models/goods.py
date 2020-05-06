
from peewee import *
from models.base import BaseModel


class GoodsCateGory(BaseModel):

    """
    商品分类表: 支持无限级扩展  业务场景限制目前最多支持3层
    """
    id = BigAutoField(primary_key=True)

    userid = BigIntegerField(verbose_name="用户代码",null=True)
    gdcgid = CharField(max_length=10,default="",verbose_name="分类代码",null=True)
    gdcgname = CharField(max_length=120, default="",verbose_name="分类名称",null=True)
    # gdcgtitle = CharField(max_length=120,default="",verbose_name="标题",null=True,blank=True)
    gdcglastid = CharField(max_length=10,default="",verbose_name="上级代码",null=True)

    level = IntegerField(verbose_name="第几层",default=1,null=True)
    sort = IntegerField(verbose_name="排序",default=0,null=True)
    status = CharField(max_length=1, default="1",verbose_name="是否上架,0-是,1-否",null=True)
    url = CharField(max_length=255,verbose_name="图片",default="")

    class Meta:
        db_table = 'goodscategory'


class Goods(BaseModel):

    """
    商品表
    """

    id = BigAutoField(primary_key=True)

    userid = BigIntegerField(verbose_name="用户代码",null=True)
    gdid = CharField(max_length=10, verbose_name="商品ID", null=True)

    gdcgid = CharField(max_length=512,default='{"gdcgids":[]}',verbose_name="分类代码",null=True)

    gdname = CharField(max_length=120, verbose_name="商品名称", default='', null=True)

    gdshowprice = DecimalField(max_digits=18,decimal_places=6,default=0.000,verbose_name="商品显示价格")
    gdshowprice1 = DecimalField(max_digits=18,decimal_places=6,default=0.000,verbose_name="商品划线价格")

    gdstockdeltype = CharField(max_length=1,verbose_name="库存扣减方式 0-加入购物车扣减,1-付款扣减,2-加入购物车扣减,一定时间系统自动清除购物车返还给库存!",default="")

    gdhavetime = IntegerField(verbose_name="当库存扣减方式为2时，此值有效,单位是分钟",default=0)

    gdtotstock = IntegerField(verbose_name="总库存",default=0)

    gdresidueshow = CharField(max_length=1,verbose_name="商品详情是否显示剩余库存! 0-显示,1-不显示",default='0')

    gdstatus = CharField(verbose_name="状态,0-上架,1-下架",default='1',max_length=1)

    sort = IntegerField(verbose_name="排序",default=0)

    gdbanners = CharField(max_length=1024,verbose_name="商品轮播图数据集合", default='{"gdbanners":[]}', null=True)

    gdsku = TextField(verbose_name="商品SKU",default='{"gdsku":[]}')

    gdcount  = CharField(max_length=512,verbose_name="商品统计数据",default='{}')

    gddetail = TextField(default="{}",verbose_name="商品详细数据")

    gdotherinfo = CharField(max_length=512,default="{}",verbose_name="""
                        "uptime" -> 上架时间
                        "willsell" -> 预售 
                            "flag" -> 0 不预售 1 预售
                            "type" -> 预售方式 0-按日期,1-付款成功后多少天
                            "value" -> 如果预售 那么此处就是指定的日期或天数
                        "limitsell" -> 限够(限制每人可购买数量)
                            "flag" -> 是否限购 0-不限购,1-限购
                            "type" -> 限购方式 0-终身限购,1-按周期限购
                            "value" ->限购数量/周期限购(年->Y,月->M,周->W,如果是按每年100件那么值就是Y,100)
                        "sharememo" -> 分享描述
                        "selltype" -> 商品卖点
                    """)

    class Meta:
        db_table = 'goods'

class GoodsLinkSku(BaseModel):

    id = BigAutoField(primary_key=True)
    gdid = CharField(max_length=10, verbose_name="商品ID", null=True)
    keyid = BigIntegerField(verbose_name="sku组ID", default=0)
    valueid = BigIntegerField(verbose_name="sku值ID", default=0)
    img = CharField(verbose_name="图片",max_length=255)
    price = DecimalField(max_digits=18,decimal_places=6,default=0.000,verbose_name="价格")
    stock = IntegerField(verbose_name="库存",default=0)
    code = CharField(max_length=60,verbose_name="规格编码",default="")
    cost_price = DecimalField(max_digits=18,decimal_places=6,default=0.000,verbose_name="成本价")
    number = IntegerField(verbose_name="销量",default=0)

    class Meta:
        db_table = 'goodslinksku'

class SkuKey(BaseModel):

    id = BigAutoField(primary_key=True)

    userid = BigIntegerField(verbose_name="用户代码",null=True)
    key = CharField(verbose_name="sku组名称",default='',max_length=60)

    class Meta:
        db_table = 'skukey'

class SkuValue(BaseModel):
    id = BigAutoField(primary_key=True)

    userid = BigIntegerField(verbose_name="用户代码", null=True)
    keyid = BigIntegerField(verbose_name="sku组名称", default=0)
    value = CharField(verbose_name="sku值名称",default="",max_length=60)

    class Meta:
        db_table = 'skuvalue'