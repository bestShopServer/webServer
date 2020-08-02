
from apps.base import BaseHandler
from services import set_dict
from utils.decorator.connector import Core_connector
from models.user import Role,User
from playhouse.shortcuts import model_to_dict
from utils.exceptions import PubErrorCustom
from utils.hash import get_token

from router import route


@route('/test')
class TestHandler(BaseHandler):

    @Core_connector()
    async def get(self, *args, **kwargs):

        role = await self.db.get(Role,rolecode='1000')
        res = model_to_dict(role)

        s = set_dict(res)

        await self.redis.set("name","张三")
        print(await self.redis.get("name"))

        return {"data":{
            "name":"张飞",
            "bal":10.312
        }}

@route()
class login(BaseHandler):

    """
    登录
    """

    @Core_connector(isTicket=False,isTransaction=False)
    async def post(self, *args, **kwargs):

        try:
            user = await self.db.get(User,uuid=self.data.get('loginname'))
        except User.DoesNotExist:
            raise PubErrorCustom("登录账户或密码错误！")

        if user.passwd != self.data.get('password'):
            raise PubErrorCustom("登录账户或密码错误！")

        if user.status == 1:
            raise PubErrorCustom("登陆账号已到期！")
        elif user.status == 2:
            raise PubErrorCustom("已冻结！")

        token = get_token()

        c = self.redisC(key=token)
        await c.set_dict(user.userid)

        return {"data":token}

@route()
class logout(BaseHandler):
    """
    登出
    """

    @Core_connector()
    async def post(self, *args, **kwargs):

        c = self.redisC(key=self.token)
        await c.del_dict()

        return None