

from apps.base import BaseHandler

from utils.decorator.connector import Core_connector
from utils.exceptions import PubErrorCustom

from router import route

from apps.app.order.rule import AddressRules
from models.order import Address

@route(None,id=True)
class address(BaseHandler):

    """
    收货地址管理
    """

    async def add_before_handler(self,**kwargs):

        address_default = self.data.get("address_default",None)
        if not address_default:
            raise PubErrorCustom("请选择是否默认!")

        if address_default == '0':
            for item in await self.db.execute(Address.select().where(Address.userid == self.user.userid)):
                item.address_default = '1'
                await self.db.update(item)

    @Core_connector(**{**AddressRules().post(),**{"add_before_handler":add_before_handler}})
    async def post(self):
        pass

    @Core_connector(**{**AddressRules().put(),**{"upd_before_handler":add_before_handler}})
    async def put(self):
        pass

    @Core_connector(**AddressRules().delete())
    async def delete(self):
        pass

    @Core_connector(**AddressRules().get())
    async def get(self):
        pass