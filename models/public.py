
from peewee import *
from models.base import BaseModel

class AttachMentGroup(BaseModel):

    """
    素材分组表
    """

    id=BigAutoField(primary_key=True)
    userid = BigIntegerField(default=0)
    name = CharField(max_length=255,verbose_name="分组名称",null=True)
    type = CharField(max_length=20,verbose_name="类型")

    class Meta:
        db_table = 'attachmentgroup'

class AttachMent(BaseModel):

    """
    素材表
    """
    id=BigAutoField(primary_key=True)
    userid = BigIntegerField(default=0)
    name = CharField(max_length=255,verbose_name="名称",null=True)
    url = CharField(max_length=255,verbose_name="地址",null=True)
    type = CharField(max_length=20, verbose_name="类型")
    grouid = IntegerField(verbose_name="分组ID",null=True,default=0)

    class Meta:
        db_table = 'attachment'


MENU_TYPES_CHOICES = (
    ('0', '菜单'),
    ('1', '按钮'),
    ('2', '内页'),
)

KEEP_CHOICES = (
    ('0', '是'),
    ('1', '否'),
)

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

    class Meta:
        db_table = 'menu'
