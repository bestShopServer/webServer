
import json
from urllib.parse import urlencode
from tornado.httpclient import AsyncHTTPClient,HTTPRequest

from utils.exceptions import PubErrorCustom

class loginBase(object):

    def __init__(self,**kwargs):

        self.app = kwargs.get("app")

class wexinLogin(loginBase):

    async def wx_auth(self):

        http_client = AsyncHTTPClient()
        url = "https://api.weixin.qq.com/sns/jscode2session?{}".format(urlencode(dict(
                js_code=self.app.data.get("js_code"),
                appid=self.app.shopsetting.appid,
                secret=self.app.shopsetting.setting_data.secert,
                grant_type="authorization_code",
            )))

        res = await http_client.fetch(HTTPRequest(url=url,method='GET'))

        response = json.loads(res.body.decode('utf8'))
        if not response.get("openid",None):
            raise PubErrorCustom("获取用户错误,腾讯接口有误!")

        return response['session_key']
