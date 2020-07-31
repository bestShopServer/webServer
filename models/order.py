
from peewee import *
from models.base import BaseModel

ORDER_STATUS_CHOICES = (
    ('0', '待付款'),
    ('1', '待发货'),
    ('2', '已发货'),
    ('3', '已完成'),
    ('4', '已取消'),
    ('5', '已关闭'),
    ('6', '退款中'),
)

ORDER_SOURCE_CHOICES = (
    ('0', '安卓APP'),
    ('1', '苹果APP'),
    ('3', '微信小程序'),
    ('4', '支付宝小程序'),
    ('5', '百度小程序'),
    ('6', '抖音小程序'),
)

ORDER_PAYTYPE_CHOICES = (
    ('0', '微信支付'),
    ('1', '支付宝支付'),
    ('2', '银联支付'),
)

class Order(BaseModel):
    """
    订单表
    """

    id = BigAutoField()
    orderid = CharField(max_length=19,verbose_name="订单ID")
    userid = BigIntegerField(verbose_name="用户代码", null=True)
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
    source = CharField(verbose_name="来源",choices=ORDER_SOURCE_CHOICES,default='0')
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
    gd_number = IntegerField(verbose_name="商品数量", default=0)
    gd_item_no = CharField(max_length=60,verbose_name="商品货号",default="")
    gd_weight = IntegerField(verbose_name="商品重量(单位克)",default=0)
    gd_sku_id = BigIntegerField(verbose_name="skulinkid  当为0代表默认规格",default=0)
    gd_sku_name = CharField(verbose_name="规格名称",default="",max_length=60)
    gd_unit = CharField(max_length=20, verbose_name="单位", default="件")

    fare_amount = DecimalField(max_digits=18, decimal_places=6, default=0.000, verbose_name="运费")
    fare_no = CharField(max_length=60,verbose_name="运单号",default="")

    class Meta:
        db_table = 'orderlist'