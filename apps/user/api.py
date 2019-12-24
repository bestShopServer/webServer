
from apps.base import BaseHandler
from utils.decorator.connector import Core_connector


class userinfo(BaseHandler):

    """
    用户
    """

    @Core_connector()
    async def get(self, *args, **kwargs):

        return {"data": {
            "userid": self.user.get("userid"),
            "loginname": self.user.get("uuid"),
            "username": self.user.get("name"),
            "avatar": 'http://allwin6666.com/nginx_upload/assets/login.jpg',
            "menu": []
        }}