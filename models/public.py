
from peewee import *
from models.base import BaseModel
from models.choices import *

class AttachMentGroup(BaseModel):

    """
    素材分组表
    """

    id = BigAutoField(primary_key=True)
    merchant_id = BigIntegerField(verbose_name="商户ID")
    name = CharField(max_length=255,verbose_name="分组名称",null=True)
    type = CharField(max_length=20,verbose_name="类型")

    class Meta:
        db_table = 'attachmentgroup'

class AttachMent(BaseModel):

    """
    素材表
    """
    id=BigAutoField(primary_key=True)
    merchant_id = BigIntegerField(verbose_name="商户ID")
    name = CharField(max_length=255,verbose_name="名称",null=True)
    url = CharField(max_length=255,verbose_name="地址",null=True)
    type = CharField(max_length=20, verbose_name="类型")
    grouid = IntegerField(verbose_name="分组ID",null=True,default=0)

    class Meta:
        db_table = 'attachment'


class Menu(BaseModel):

    """
    菜单表
    """

    id = BigAutoField(primary_key=True)
    parent_id = BigIntegerField(default=0,verbose_name="父级id")
    title = CharField(max_length=255,verbose_name="标题",default="")
    type = CharField(max_length=1,verbose_name="类型",choices=MENU_TYPES_CHOICES,default="0")
    pic = CharField(max_length=255,verbose_name="图标",default="")
    sort = IntegerField(default=0,verbose_name="排序")
    component = CharField(max_length=255,verbose_name="前端组件",default="")
    component_name = CharField(max_length=255,verbose_name="组件名称",default="")
    path = CharField(max_length=255,verbose_name="地址",default="")
    keep = CharField(max_length=1,verbose_name="是否缓冲",default="1",choices=KEEP_CHOICES)

    premission = CharField(max_length=60,verbose_name="权限标识",default="")
    status = CharField(max_length=1, verbose_name="状态", choices=STATUS_CHOICES, default='0')

    class Meta:
        db_table = 'menu'

class DeleteHandlerSave(BaseModel):

    """
    数据删除记录表
    """

    id = BigAutoField(primary_key=True)
    table = CharField(max_length=60,verbose_name="表名",default="")
    key = BigIntegerField()
    operator_userid = BigIntegerField(default=0)

    class Meta:
        db_table = 'delete_handler_save'