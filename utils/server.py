import asyncio
import tornado.web
import tornado.ioloop

from tornado.options import options

from utils.database import RedisPool,MysqlPool
from loguru import logger
from router import urlpattern
from config import common


class Server(object):

    def __init__(self):
        pass

    def make_app(self,loop):
        """
        加载app
        :param loop:
        :return:
        """
        #初始化日志管理
        logger.add("logs/api.log",enqueue=True,rotation="00:00:01")

        #初始化web application
        apps = tornado.web.Application(handlers=urlpattern,default_host=None,transforms=None,**common)

        #初始化redis
        apps.redis = RedisPool(loop=loop).get_conn()

        #初始化mysql
        apps.mysql = MysqlPool().get_manager

        return apps

    def start(self):
        try:
            logger.info("server start...")
            loop = asyncio.get_event_loop()
            app = self.make_app(loop)
            app.listen(options.common_port)
            logger.info("port: {}".format(options.common_port))
            loop.run_forever()
        except KeyboardInterrupt:
            logger.info("server stop")