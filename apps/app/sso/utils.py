
import json
from urllib.parse import urlencode
from tornado.httpclient import AsyncHTTPClient,HTTPRequest

from utils.exceptions import PubErrorCustom
import base64
import json

from models.user import User
from utils.hash import get_token

from cryptokit import AESCrypto

from apps.app.sso.serializers import UserForAppSerializer

class WXBizDataCrypt:
    def __init__(self, appId, sessionKey):
        self.appId = appId
        self.sessionKey = sessionKey

    def decrypt(self, encryptedData, iv):
        # base64 decode
        sessionKey = base64.b64decode(self.sessionKey)
        encryptedData = base64.b64decode(encryptedData)
        iv = base64.b64decode(iv)

        cipher = AESCrypto(sessionKey, iv)
        decrypted = json.loads(cipher.decrypt(encryptedData))

        if decrypted['watermark']['appid'] != self.appId:
            raise Exception('Invalid Buffer')

        return decrypted


class loginBase(object):

    def __init__(self,**kwargs):

        self.app = kwargs.get("app")
        self.appid = kwargs.get("appid","wxf09e1a6a0ee3dd1b")
        self.secret = kwargs.get("secret","a7b66d8f92dfb21f95a6e93face4a3ca0")

class wexinLogin(loginBase):

    async def wx_auth(self):

        http_client = AsyncHTTPClient()
        url = "https://api.weixin.qq.com/sns/jscode2session?{}".format(urlencode(dict(
                js_code=self.app.data.get("js_code"),
                appid=self.appid,
                secret=self.secret,
                grant_type="authorization_code",
            )))

        res = await http_client.fetch(HTTPRequest(url=url,method='GET'))

        response = json.loads(res.body.decode('utf8'))
        if not response.get("openid",None):
            raise PubErrorCustom("获取用户错误,腾讯接口有误!")

        data=None

        try:
            user=await self.app.db.get(User,uuid=response.get('openid'))
            token = get_token()

            user.token = token

            data = UserForAppSerializer(user,many=False).data

            await self.app.redis.set(token,user.userid)

        except User.DoesNotExist:
            pass

        return {"data":{
            "user" : data,
            "session_key":response.get("session_key")
        }}

    async def wx_login(self):

        res = self.decrypt()

        try:
            user = await self.app.db.get(User,uuid=res.get('openid'))
        except User.DoesNotExist:

            user = await self.app.db.create(User,**{
                "uuid": res.get('openId') if 'unionId' not in res else res['unionId'],
                "rolecode": '4001',
                "mobile": res.get('openId') if 'unionId' not in res else res['unionId'],
                "name": res.get("nickName"),
                "sex": res.get("sex"),
                "addr": "{}-{}-{}".format(res.get("country"), res.get("city"), res.get("province")),
                "pic": res.get("avatarUrl")
            })

        token = get_token()

        user.token = token

        data = UserForAppSerializer(user, many=False).data

        await self.app.redis.set(token, user.userid)

        return {"data":data}

    def decrypt(self):

        encryptedData = self.app.data.get("encryptedData")
        sessionKey = self.app.data.get("sessionKey")
        iv = self.app.data.get("iv")

        encryptedData = base64.b64decode(encryptedData)

        iv = base64.b64decode(iv)

        cipher = AESCrypto(base64.b64decode(sessionKey), iv)
        decrypted = json.loads(cipher.decrypt(encryptedData))

        if decrypted['watermark']['appid'] != self.appid:
            raise Exception('Invalid Buffer')

        return decrypted
