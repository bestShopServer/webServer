


import json
from apps.base import BaseHandler

from utils.decorator.connector import Core_connector
from utils.exceptions import PubErrorCustom

from router import route

from apps.lib.login.login_by_wechat import wechatLogin

@route()
class wexin_auth(BaseHandler):

    """
    微信授权登录
    """

    @Core_connector(isTicket=False)
    async def post(self):

        return await wechatLogin(app=self).wx_auth()


@route()
class wexin_login(BaseHandler):
    """
    微信登录
    """

    @Core_connector(isTicket=False)
    async def post(self):
        return await wechatLogin(app=self).wx_login()