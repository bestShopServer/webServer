
from peewee import *
from models.base import BaseModel


class AttachMentGroup(BaseModel):

    id=AutoField(primary_key=True)
    userid = BigIntegerField(default=0)
    name = CharField(max_length=255,verbose_name="分组名称",null=True)
    number = IntegerField(default=0,verbose_name="数量",null=True)
    type = CharField(max_length=20,verbose_name="类型")

    class Meta:
        db_table = 'attachmentgroup'

class AttachMent(BaseModel):

    id=AutoField(primary_key=True)
    userid = BigIntegerField(default=0)
    name = CharField(max_length=255,verbose_name="名称",null=True)
    url = CharField(max_length=255,verbose_name="地址",null=True)
    grouid = IntegerField(verbose_name="分组ID",null=True)

    class Meta:
        db_table = 'attachment'
