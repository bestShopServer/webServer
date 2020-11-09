
from apps.lib.login.base import LoginBase
from models.user import User,UserAuth
from utils.hash import get_token

from utils.exceptions import PubErrorCustom

class loginNameLogin(LoginBase):

    """
    登录账号密码登录
    """

    def __init__(self,**kwargs):

        self.login_type = '0'

        super(loginNameLogin, self).__init__(**kwargs)

    async def login(self):

        account = self.app.data.get("loginname",None)
        ticket = self.app.data.get('password',None)

        res = await self.app.db.execute(
            UserAuth.select().where(
                UserAuth.account == account,
                UserAuth.ticket == ticket,
                UserAuth.is_password == '0'
            )
        )

        if not len(res):
            raise PubErrorCustom("登录账号或密码错误!")

        user = await self.app.db.get(User, userid=res[0].userid)
        self.check_status(user.status)

        token = get_token()

        await self.app.redis.set(token, user.userid)

        return {"data":token}