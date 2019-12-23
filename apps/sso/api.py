
from apps.base import BaseHandler
from services import set_dict
from utils.decorator.connector import Core_connector
from models.user import Role,User
from playhouse.shortcuts import model_to_dict
from utils.exceptions import PubErrorCustom
from utils.hash import get_token

class TestHandler(BaseHandler):

    @Core_connector()
    async def get(self, *args, **kwargs):
        # Role(name="1123")

        # raise PubErrorCustom("12312321312")
        role = await self.db.get(Role,rolecode='1000')
        res = model_to_dict(role)

        s = set_dict(res)
        # #
        # # print(role.name)
        # logger.debug("123123fsds")

        await self.redis.set("name","张三")
        print(await self.redis.get("name"))

        return {"data":{
            "name":"张飞",
            "bal":10.312
        }}


class LoginHandler(BaseHandler):

    @Core_connector(isPasswd=True)
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
        await c.set_dict(value={
            "userid":user.userid,
            "rolecode":user.rolecode,
            "uuid": user.uuid,
            "name":user.name,
            "pic": user.pic
        })

        return {"data":token}

