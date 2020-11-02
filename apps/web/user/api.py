
from apps.base import BaseHandler
from utils.decorator.connector import Core_connector
from router import route

from models.user import Merchant

@route()
class userinfo(BaseHandler):

    """
    用户
    """

    @Core_connector()
    async def get(self, *args, **kwargs):

        return {"data": {
            "userid": self.user.userid,
            "merchant_id": self.user.merchant_id,
            "username": self.user.name,
            "rolecode":self.user.role_code,
            "avatar": 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1604320145113&di=c0f37be5cc6331c65ec5773edbf7c1da&imgtype=0&src=http%3A%2F%2Fb-ssl.duitang.com%2Fuploads%2Fitem%2F201703%2F18%2F20170318012043_H4mRj.jpeg',
            "menu": []
        }}