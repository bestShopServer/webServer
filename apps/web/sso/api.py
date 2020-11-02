
from apps.base import BaseHandler
from utils.decorator.connector import Core_connector

from utils.exceptions import PubErrorCustom

from apps.lib.login.login_by_loginname import loginNameLogin

from router import route


# @route('/test')
# class TestHandler(BaseHandler):
#
#     @Core_connector()
#     async def get(self, *args, **kwargs):
#
#         role = await self.db.get(Role,rolecode='1000')
#         res = model_to_dict(role)
#
#         s = set_dict(res)
#
#         await self.redis.set("name","张三")
#         print(await self.redis.get("name"))
#
#         return {"data":{
#             "name":"张飞",
#             "bal":10.312
#         }}

@route()
class login(BaseHandler):

    """
    登录
    """

    @Core_connector(isTicket=False,isTransaction=False)
    async def post(self, *args, **kwargs):

        return await loginNameLogin(app=self).login()

@route()
class logout(BaseHandler):
    """
    登出
    """

    @Core_connector()
    async def post(self, *args, **kwargs):

        await loginNameLogin(app=self).login_out()