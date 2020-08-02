
from tornado.web import RequestHandler
from aioredis import Redis

from services.cache.base import RedisBase
from utils.idGenerator import idGenerator
from utils.exceptions import PubErrorCustom

class BaseHandler(RequestHandler):

    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header('Access-Control-Max-Age', 1000)
        self.set_header('Content-type', 'application/json')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, DELETE, PUT, PATCH, OPTIONS')
        self.set_header('Access-Control-Allow-Headers',
                        'Content-Type,Platform,Appid,x-count,Authorization,Access-Control-Allow-Origin, Access-Control-Allow-Headers, X-Requested-By, Access-Control-Allow-Methods')

    def options(self, *args, **kwargs):
        pass

    @property
    def db(self):
        """
        mysql操作对象
        :return:
        """
        return self.application.mysql

    @property
    def redis(self) -> Redis:
        """
        redis操作对象
        :return:
        """
        return self.application.redis

    def checkvoid(self,key,memo):

        if not self.data.get(key,None):
            raise PubErrorCustom(memo)

    def checkmodelvoid(self,model,keys):
        for key in keys:
            if not self.data.get(key, None):
                raise PubErrorCustom("{}为空!".format(                getattr(model,key).verbose_name))

    def redisC(self,key):
        """
        redis操作集合
        :param key:
        :return:
        """
        return RedisBase(redis=self.redis,key=key)

    def idGeneratorClass(self):
        """
        id生成器
        :return:
        """
        return idGenerator(redis=self.redis)

    def get_model_table_name(self,model):
        return model._meta.table_name

    def get_model_auto_increment_key(self,model):

        return model._meta.primary_key.name