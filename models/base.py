
from peewee import *

from utils.time_st import MyTime
from utils.database.mysql import MysqlPool

class BaseModel(Model):

    createtime = BigIntegerField(default=0, verbose_name="创建时间")
    updtime = BigIntegerField(default=0, verbose_name="修改时间")

    class Meta:
        database = MysqlPool().get_conn
        legacy_table_names = False
