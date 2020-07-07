


from utils.decorator.utils.base import ConnectorFuncsBase

from utils.exceptions import PubErrorCustom,InnerErrorCustom

class ConnectorTicket(ConnectorFuncsBase):

    async def run(self):
        """
        令牌处理
        """
        if self.connector.isTicket:
            token = self.connector_app.request.headers.get_list("Authorization")
            if len(token) <= 0:
                raise InnerErrorCustom(code="20001", msg="拒绝访问!")
            else:
                token = token[0]
            c = self.connector_app.redisC(key=token)
            result = await c.get_dict()

            if not result:
                raise InnerErrorCustom(code="20002", msg="拒绝访问")

            if result.get("status") == '1':
                raise PubErrorCustom("账户已到期!")
            elif result.get("status") == '2':
                raise PubErrorCustom("账户已冻结!")

            self.connector_app.user = result
            self.connector_app.token = token