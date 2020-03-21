
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

    gdcgid1 = CharField(max_length=10,default="",verbose_name="分类代码1",null=True)
    gdcgid2 = CharField(max_length=10,default="",verbose_name="分类代码2",null=True)
    gdcgid3 = CharField(max_length=10,default="",verbose_name="分类代码3",null=True)

    gdname = CharField(max_length=120, verbose_name="商品名称", default='', null=True)
    gdtext = CharField(max_length=255, verbose_name="分享描述", default='', null=True)
    gdpricetext = CharField(max_length=255, verbose_name="商品卖点", default='', null=True)
    gdstatus = CharField(verbose_name="状态,0-上架,1-下架",default='0',max_length=1)

    sendinfomation = CharField(max_length=1024,default='{"sendtype":"111"}',
                               verbose_name="物流信息,配置方式,第一位代表快递发货,第二位代表同城配送,第三位代表到店自提,0-开启,1-停用")

    gdnum  = IntegerField(verbose_name="商品库存",default=0)
    sort = IntegerField(verbose_name="排序",default=0)

    gdbanners = TextField(verbose_name="商品轮播图数据集合", default='{"banners":[]}', null=True)

    sku = TextField(verbose_name="商品SKU",default='{"sku":[]}')

    qrcode = CharField(verbose_name="商品二维码",default='',max_length=255)
    hb = CharField(verbose_name="海报",default="",max_length=255)
    gdcount  = CharField(max_length=1024,verbose_name="商品统计数据",default='{}')
    detail = TextField(default="{}",verbose_name="商品详细数据")

    class Meta:
        db_table = 'goods'
