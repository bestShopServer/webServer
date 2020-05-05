
from peewee import *

from utils.time_st import MyTime
from utils.database.mysql import MysqlPool



class BaseModel(Model):

    createtime = BigIntegerField(default=0, verbose_name="创建时间")
    updtime = BigIntegerField(default=0, verbose_name="修改时间")

    def save(self, *args, **kwargs):

        self.createtime = MyTime().timestamp

        if not self.createtime:
            self.createtime = MyTime().timestamp

        return super(BaseModel, self).save(*args, **kwargs)

    class Meta:
        # table_name = 'users'
        database = MysqlPool().get_conn
        legacy_table_names = False
