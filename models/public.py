
from peewee import *
from models.base import BaseModel


class AttachMentGroup(BaseModel):

    id=AutoField(primary_key=True)
    name = CharField(max_length=255,verbose_name="分组名称",null=True)
    number = IntegerField(default=0,verbose_name="数量",null=True)

    class Meta:
        db_table = 'attachmentgroup'

class AttachMent(BaseModel):

    id=AutoField(primary_key=True)
    url = CharField(max_length=255,verbose_name="地址",null=True)
    title = CharField(max_length=255,verbose_name="名称",null=True)
    grouid = IntegerField(verbose_name="分组ID",null=True)
    type   = CharField(max_length=255,verbose_name="类型",null=True)

    class Meta:
        db_table = 'attachment'
