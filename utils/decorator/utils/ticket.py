
from utils.decorator.utils.base import ConnectorFuncsBase

from utils.exceptions import PubErrorCustom,InnerErrorCustom

from models.user import User

class ConnectorTicket(ConnectorFuncsBase):

    async def run(self):
        """
        令牌处理
        """
        if self.connector.isTicket:
            token = self.connector_app.request.headers.get_list("Authorization")
            if len(token) <= 0:
                raise InnerErrorCustom(code="20001", msg="令牌失效!")
            else:
                token = token[0]
            c = self.connector_app.redisC(key=token)
            result = await c.get_dict()

            if not result:
                raise InnerErrorCustom(code="20002", msg="令牌失效!")

            try:
                self.connector_app.user = await self.connector_app.db.get(User, userid=result)
            except User.DoesNotExist:
                raise PubErrorCustom("账户不存在!")

            if self.connector_app.user.status == '1':
                raise PubErrorCustom("账户已到期!")
            elif self.connector_app.user.status == '2':
                raise PubErrorCustom("账户已冻结!")

            self.connector_app.token = token