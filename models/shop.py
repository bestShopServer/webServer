

from peewee import *
from models.base import BaseModel

class ShopPage(BaseModel):
    """
    微页面
    """
    id = BigAutoField(primary_key=True)
    userid = BigIntegerField(verbose_name="用户代码",null=True)
    title = CharField(max_length=60,verbose_name="名称",default="")
    time_publish_flag = CharField(max_length=1,verbose_name="是否定时发布 0-是,1-否",default='1')
    time_publish = BigIntegerField(default=0,verbose_name="发布时间")
    html_data = TextField(default="{}")

    class Meta:
        db_table = 'shoppage'