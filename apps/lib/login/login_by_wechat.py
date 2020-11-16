
from utils.exceptions import PubErrorCustom
import base64
import json

from models.user import User,UserAuth
from utils.hash import get_token

from cryptokit import AESCrypto
from loguru import logger

from apps.app.sso.serializers import UserForAppSerializer

from apps.lib.login.base import LoginBase

from utils.httpRequest import HttpRequestCustom

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

class wechatLogin(LoginBase):

    """
    微信小程序授权登录
    """

    def __init__(self,**kwargs):

        self.appid = kwargs.get("appid","wx2c4649a77ef8edcd")
        self.secret = kwargs.get("secret","c1c631ac430353eac46b9e90d048d7cc")

        self.login_type = '5'
        self.role_type = '2'

        super(wechatLogin, self).__init__(**kwargs)

    async def wx_auth(self):

        response = await HttpRequestCustom(
            url="https://api.weixin.qq.com/sns/jscode2session",
            params=dict(
                js_code=self.app.data.get("js_code"),
                appid=self.appid,
                secret=self.secret,
                grant_type="authorization_code",
            )
        )

        if response['errcode'] != 0:
            raise PubErrorCustom(response['errmsg'])

        return {"data":{
            "user" : None,
            "session_key":response['session_key']
        }}

    async def wx_login(self):

        res = self.decrypt()
        logger.info("小程序用户信息=>{}".format(res))

        account = res.get('openId') if 'unionId' not in res else res['unionId']

        try:
            user_auth_obj = await self.app.db.get(UserAuth,
                        account=account,
                        type=self.login_type)

            user = await self.app.db.get(User, userid=user_auth_obj.userid)

            user.name = res.get("nickName")
            user.sex = res.get("sex")
            user.address = "{}-{}-{}".format(res.get("country"), res.get("city"), res.get("province"))
            user.pic = res.get("avatarUrl")

            await self.app.db.update(user)
            self.check_status(user.status)
        except UserAuth.DoesNotExist:

            user = await self.app.db.create(User,**{
                "role_type": self.role_type,
                "name": res.get("nickName"),
                "sex": res.get("sex"),
                "address": "{}-{}-{}".format(res.get("country"), res.get("city"), res.get("province")),
                "pic": res.get("avatarUrl")
            })

            await self.app.db.create(UserAuth,**{
                "userid":user.userid,
                "type":self.login_type,
                "account":account
            })

        token = get_token()

        user.token = token

        data = UserForAppSerializer(user, many=False).data

        await self.app.redisC(key=token).set_dict({
            "userid":user.userid
        })

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
