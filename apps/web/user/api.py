
from apps.base import BaseHandler
from utils.decorator.connector import Core_connector
from router import route


@route()
class userinfo(BaseHandler):

    """
    用户
    """

    @Core_connector()
    async def get(self, *args, **kwargs):

        return {"data": {
            "userid": self.user.userid,
            "loginname": self.user.uuid,
            "username": self.user.name,
            "rolecode":self.user.rolecode,
            "avatar": 'http://allwin6666.com/nginx_upload/assets/login.jpg',
            "menu": []
        }}