import asyncio

from tornado.options import options

from utils.database import RedisPool,MysqlPool
from loguru import logger
from utils.app import Application

from utils.time_st import UtilTime


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

        # logger.add("logs/api.log",enqueue=True,rotation="00:00:01",backtrace=True,retention='10 days')
        logger.add("logs/api.log",rotation="00:00:01",retention='10 days',enqueue=True,encoding='utf-8',backtrace=True, diagnose=True)
        # logger.remove(logserver)

        #初始化web application
        apps =  Application()

        #初始化redis
        apps.redis = RedisPool(loop=loop).get_conn()

        #初始化mysql
        apps.mysql = MysqlPool().get_manager

        return apps

    def start(self):
        try:
            logger.info(UtilTime().arrow_to_string())
            logger.info("server start...")
            loop = asyncio.get_event_loop()
            app = self.make_app(loop)
            app.listen(options.common_port)
            logger.info("port: {}".format(options.common_port))
            loop.run_forever()
        except KeyboardInterrupt:
            logger.info("server stop")