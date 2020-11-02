

from utils.exceptions import PubErrorCustom

class LoginBase(object):

    def __init__(self,**kwargs):

        self.app = kwargs.get("app")

    @staticmethod
    def check_status(status):

        if status != '0':
            raise PubErrorCustom("账号状态异常!")

    async def login_out(self):
        await self.app.redis.delete(self.app.token)