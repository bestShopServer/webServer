
from utils.decorator.utils.base import ConnectorFuncsBase

from utils.exceptions import PubErrorCustom,InnerErrorCustom

from models.user import User,Merchant

from utils.time_st import UtilTime

class ConnectorTicket(ConnectorFuncsBase):


    async def get_token(self):
        token = self.connector_app.request.headers.get_list("Authorization")
        self.connector_app.token = token

        if len(token) <= 0:
            raise InnerErrorCustom(code="20001", msg="用户令牌失效!")
        else:
            token = token[0]
        c = self.connector_app.redisC(key=token)
        res = await c.get_dict()

        if not res:
            raise InnerErrorCustom(code="20002", msg="用户令牌失效!")

        self.token_data = res

    async def user_handler(self):

        try:
            self.connector_app.user = await self.connector_app.db.get(User, userid=self.token_data.get("userid",None))
            self.connector_app.user.merchant_id = self.token_data.get("merchant_id",0)

        except User.DoesNotExist:
            raise InnerErrorCustom(code="20003", msg="用户已关闭!")

        if self.connector_app.user.status == '1':
            raise InnerErrorCustom(code="20003", msg="用户已关闭!")
        elif self.connector_app.user.status == '2':
            raise InnerErrorCustom(code="20004", msg="用户已冻结!")

    async def merchant_hander(self):

        merchant_id = self.token_data.get("merchant_id", None)
        if self.connector_app.user.role_type == '1' and merchant_id:
            merchant_id = self.token_data.get("merchant_id",None)

            try:
                self.connector_app.merchant = await self.connector_app.db.get(Merchant, merchant_id=merchant_id)

            except Merchant.DoesNotExist:
                raise InnerErrorCustom(code="30001", msg="租户已关闭!")

            if self.connector_app.merchant.status == '1':
                raise InnerErrorCustom(code="30001", msg="租户已关闭!")

            if self.connector_app.merchant.expire_time <= UtilTime().timestamp:
                raise InnerErrorCustom(code="30002", msg="租户已过期!")
        elif self.connector_app.user.role_type == '1' and not merchant_id:
            raise InnerErrorCustom(code="20005", msg="非法租户!")

    async def app_run(self):
        await self.user_handler()

    async def web_run(self):

        await self.user_handler()
        await self.merchant_hander()

    async def run(self):
        """
        令牌处理
        """

        if self.connector.isTicket:

            await self.get_token()

            if self.platform == 'app':
                await self.app_run()
            elif self.platform == 'web':
                await self.web_run()