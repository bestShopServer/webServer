
from tornado.web import RequestHandler
from aioredis import Redis

from services.cache.base import RedisBase


class BaseHandler(RequestHandler):

    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header('Access-Control-Max-Age', 1000)
        self.set_header('Content-type', 'application/json')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, DELETE, PUT, PATCH, OPTIONS')
        self.set_header('Access-Control-Allow-Headers',
                        'Content-Type, Authorization,Access-Control-Allow-Origin, Access-Control-Allow-Headers, X-Requested-By, Access-Control-Allow-Methods')

        print(self._headers)

    def options(self, *args, **kwargs):
        pass

    @property
    def db(self):
        return self.application.mysql

    @property
    def redis(self) -> Redis:
        return self.application.redis

    def redisC(self,key):
        return RedisBase(redis=self.redis,key=key)
