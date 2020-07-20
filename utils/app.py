
import tornado.web
from config import common
from router import route

from importlib import import_module
import os

from loguru import logger


class LoadModule(object):

    def __init__(self):
        self.basedir = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), "apps")
        self.appdir = os.path.join(self.basedir, "app")
        self.webdir = os.path.join(self.basedir, "web")

    def run(self):

        for item in os.listdir(self.appdir):
            try:
                import_module("apps.app.{}.api".format(item))
            except ModuleNotFoundError :
                pass

        for item in os.listdir(self.webdir):
            try:
                import_module("apps.web.{}.api".format(item))
            except ModuleNotFoundError :
                pass


LoadModule().run()

class Application(tornado.web.Application):

    def __init__(self):
        logger.info("\n路由表->{}".format(route.urls, indent=4))
        super().__init__(handlers=route.urls,default_host=None,transforms=None,**common)

    # def route(self, url):
    #     """
    #     :param url: URL地址
    #     :return: 注册路由关系对应表的装饰器
    #     """
    #
    #     urlnew = "/{}{}".format(common.get("version","v1"),common.get("api_base","/api"))
    #     def register(handler):
    #         """
    #         :param handler: URL对应的Handler
    #         :return: Handler
    #         """
    #         print(handler)
    #         self.add_handlers(".*$", [(urlnew, handler)])  # URL和Handler对应关系添加到路由表中
    #         return handler
    #
    #     return register