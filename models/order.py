
from peewee import *
from models.base import BaseModel
from models.choices import *

class OrderRefund(BaseModel):
    """
    退款表
    """

    id = BigAutoField()
    refund_id = CharField(max_length=19,verbose_name="退款ID")
    orderid = CharField(max_length=19,verbose_name="订单ID")
    status = CharField(max_length=1,verbose_name="退款状态",choices=REFUND_STATUS_CHOICES)
    pay_amount = DecimalField(verbose_name="订单金额", max_digits=18, decimal_places=6, default=0.0)
    refund_amount = DecimalField(verbose_name="退款金额", max_digits=18, decimal_places=6, default=0.0)

    class Meta:
        db_table = 'refund'

class Order(BaseModel):
    """
    订单表
    """

    id = BigAutoField()
    orderid = CharField(max_length=19,verbose_name="订单ID")
    userid = BigIntegerField(verbose_name="用户代码", null=True)
    super_userid = BigIntegerField(verbose_name="商铺管理员用户代码",null=True)
    status = CharField(max_length=1,choices=ORDER_STATUS_CHOICES,verbose_name="状态",default="0")
    status_list = CharField(max_length=2048,
                            verbose_name="""
                                {
                                    "status":状态,
                                    "time":时间
                                }    
                            """,default="[]")

    price = DecimalField(verbose_name="商品总价",max_digits=18,decimal_places=6,default=0.0)
    fare_amount = DecimalField(verbose_name="运费",max_digits=18,decimal_places=6,default=0.0)
    pay_amount = DecimalField(verbose_name="实际支付金额", max_digits=18, decimal_places=6, default=0.0)

    trade_no = CharField(max_length=60,verbose_name="外部订单号",default="")

    class Meta:
        db_table = 'order'

class OrderDetail(BaseModel):

    """
    订单详情表
    """
    id = BigAutoField()
    orderid = CharField(max_length=19, verbose_name="订单ID")

    memo = CharField(verbose_name="买家备注",default="",max_length=60)
    source = CharField(max_length=1,verbose_name="来源",choices=ORDER_SOURCE_CHOICES,default='3')
    pay_type = CharField(max_length=1,verbose_name="支付方式",default="0",choices=ORDER_PAYTYPE_CHOICES)

    name = CharField(max_length=60, verbose_name="收货人", default='')
    phone = CharField(max_length=60, verbose_name="收货电话", default='')

    province_code = CharField(max_length=20, verbose_name="省code", default="")
    province_name = CharField(max_length=20, verbose_name="省名称", default="")

    city_code = CharField(max_length=20, verbose_name="市code", default="")
    city_name = CharField(max_length=20, verbose_name="市名称", default="")

    county_code = CharField(max_length=20, verbose_name="市code", default="")
    county_name = CharField(max_length=20, verbose_name="市名称", default="")

    detail = CharField(max_length=1024, verbose_name="地址", default="")

    class Meta:
        db_table = 'orderdetail'


class OrderList(BaseModel):
    """
    订单明细表
    """

    id = BigAutoField()
    orderid = CharField(max_length=19, verbose_name="订单ID")
    gdid = BigIntegerField(verbose_name="商品ID")

    gd_img = CharField(max_length=255, verbose_name="图片", default='')
    gd_name = CharField(max_length=120, verbose_name="商品名称",default="")
    gd_price = DecimalField(max_digits=18, decimal_places=6, default=0.000, verbose_name="商品价格(单价)")
    gd_number = IntegerField(verbose_name="购买数量", default=0)
    gd_item_no = CharField(max_length=60,verbose_name="商品货号",default="")
    gd_weight = IntegerField(verbose_name="商品重量(单位克)",default=0)
    gd_sku_id = BigIntegerField(verbose_name="skulinkid  当为0代表默认规格",default=0)
    gd_sku_name = CharField(verbose_name="规格名称",default="",max_length=60)
    gd_unit = CharField(max_length=20, verbose_name="单位", default="件")

    fare_amount = DecimalField(max_digits=18, decimal_places=6, default=0.000, verbose_name="运费")
    fare_no = CharField(max_length=60,verbose_name="运单号",default="")

    fare_status = CharField(max_length=1,verbose_name="发货状态,0-已发货,1-未发货")

    class Meta:
        db_table = 'orderlist'

class ShopCart(BaseModel):
    """
    购物车表
    """

    id = BigAutoField()
    gdid = BigIntegerField(verbose_name="商品ID")
    userid = BigIntegerField(verbose_name="用户代码", null=True)

    gd_img = CharField(max_length=255, verbose_name="图片", default='')
    gd_name = CharField(max_length=120, verbose_name="商品名称",default="")
    gd_price = DecimalField(max_digits=18, decimal_places=6, default=0.000, verbose_name="商品价格(单价)")
    gd_number = IntegerField(verbose_name="购买数量", default=0)
    gd_item_no = CharField(max_length=60,verbose_name="商品货号",default="")
    gd_weight = IntegerField(verbose_name="商品重量(单位克)",default=0)
    gd_sku_id = BigIntegerField(verbose_name="skulinkid  当为0代表默认规格",default=0)
    gd_sku_name = CharField(verbose_name="规格名称",default="",max_length=60)
    gd_unit = CharField(max_length=20, verbose_name="单位", default="件")

    class Meta:
        db_table = 'shopcart'


class Address(BaseModel):

    """
    收货地址
    """

    id = BigAutoField(primary_key=True,verbose_name="ID")
    userid = BigIntegerField(verbose_name="用户代码",null=True)

    name = CharField(max_length=60,verbose_name="收获人",default='')
    mobile = CharField(max_length=60,verbose_name="收货手机号",default='')

    province_code = CharField(max_length=20, verbose_name="省code", default="")
    province_name = CharField(max_length=20, verbose_name="省名称", default="")

    city_code = CharField(max_length=20, verbose_name="市code", default="")
    city_name = CharField(max_length=20, verbose_name="市名称", default="")

    county_code = CharField(max_length=20, verbose_name="市code", default="")
    county_name = CharField(max_length=20, verbose_name="市名称", default="")

    address_detail = CharField(max_length=1024,verbose_name="详细地址",default="")
    address_default = CharField(max_length=1,verbose_name="默认,0-是,1-否",default='0')

    class Meta:
        db_table = 'address'