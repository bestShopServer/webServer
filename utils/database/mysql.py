
import os,sys

from peewee_async import PooledMySQLDatabase
from models.custom_func import ManagerSon




class MysqlPool:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            PROJECT_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.path.pardir)
            if PROJECT_PATH not in sys.path:
                sys.path.insert(0, PROJECT_PATH)

            from config import mysql
            cls.conn = PooledMySQLDatabase(
                mysql['name'],
                host=mysql['host'],
                password=mysql['password'],
                port=mysql['port'],
                user=mysql['user'],
                min_connections=mysql['min_connections'],
                max_connections=mysql['max_connections'],
                charset=mysql['charset'])
            cls.manager = ManagerSon(cls.conn)
            cls.conn.set_allow_sync(False)
            cls._instance = super(MysqlPool, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    @property
    def get_conn(self):
        return self.conn

    @property
    def get_manager(self):
        return self.manager
