

from peewee import *
from models.base import BaseModel

class ShopPage(BaseModel):
    """
    微页面
    """
    id = BigAutoField(primary_key=True)
    userid = BigIntegerField(verbose_name="用户代码",null=True)
    title = CharField(max_length=60,verbose_name="名称")
    type = IntegerField(verbose_name="几级分类",default=1)

    class Meta:
        db_table = 'goodscategorystyle'