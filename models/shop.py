

from peewee import *
from models.base import BaseModel

class ShopPage(BaseModel):
    """
    微页面
    """
    id = BigAutoField(primary_key=True)
    userid = BigIntegerField(verbose_name="用户代码",null=True)
    title = CharField(max_length=60,verbose_name="名称",default="")
    type = CharField(max_length=1,verbose_name="类型  '0'-首页,'1'-商品详情,'9'-其它",default='9')
    time_publish_flag = CharField(max_length=1,verbose_name="是否定时发布 0-是,1-否",default='1')
    time_publish = BigIntegerField(default=0,verbose_name="发布时间")
    html_data = TextField(default="{}")

    class Meta:
        db_table = 'shoppage'

class ShopConfig(BaseModel):

    """
    店铺基础信息配置
    """

    id=BigIntegerField(primary_key=True)
    userid = BigIntegerField(verbose_name="用户ID")
    navigation_data = TextField(verbose_name="导航栏设置数据",default="[]")

    class Meta:
        db_table = 'shopconfig'

class ShopSetting(BaseModel):

    """
    店铺基础信息配置
    """

    id=BigIntegerField(primary_key=True)
    userid = BigIntegerField(verbose_name="用户ID")
    platform = CharField(max_length=30,verbose_name="平台编码",default="MP-WEXIN")
    appid = CharField(max_length=60,verbose_name="APPID",default="")
    setting_data = TextField(verbose_name="配置基础数据", default="{}")

    """
    {
        "secret":"secret"
    }
    """

    class Meta:
        db_table = 'shopsetting'