
from peewee import *

from utils.time_st import MyTime
from utils.database.mysql import MysqlPool



class BaseModel(Model):

    createtime = BigIntegerField(default=0, verbose_name="创建时间")
    updtime = BigIntegerField(default=0, verbose_name="修改时间")

    def create(self, **query):
        self.createtime = MyTime().timestamp
        return super(BaseModel, self).create(self,**query)

    def update(self, __data=None, **update):
        self.updtime = MyTime().timestamp
        return super(BaseModel, self).update(self, __data=__data, **update)

    class Meta:
        # table_name = 'users'
        database = MysqlPool().get_conn
        legacy_table_names = False
