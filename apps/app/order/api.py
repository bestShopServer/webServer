

from apps.base import BaseHandler

from utils.decorator.connector import Core_connector
from utils.exceptions import PubErrorCustom

from router import route

from apps.app.order.rule import AddressRules
from models.order import Address

from models.order import ShopCart
from models.goods import Goods

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
    async def post(self, *args, **kwargs):
        pass

    @Core_connector(**{**AddressRules().put(),**{"upd_before_handler":add_before_handler}})
    async def put(self, *args, **kwargs):
        pass

    @Core_connector(**AddressRules().delete())
    async def delete(self, *args, **kwargs):
        pass

    @Core_connector(**AddressRules().get())
    async def get(self, pk=None):
        pass


@route(None,id=True)
class shopcart(BaseHandler):

    @Core_connector()
    async def post(self, *args, **kwargs):

        for shopcart in self.data.get("shopcart",[]):

            number = shopcart.get("number",None)
            gdid = shopcart.get("gdid",None)
            gd_sku_id = shopcart.get("gd_sku_id",None)
            gd_sku_name = shopcart.get("gd_sku_name",None)

            if not number:
                raise PubErrorCustom("数量非法!")
            if not gdid:
                raise PubErrorCustom("商品ID非法!")
            if gd_sku_id == None:
                raise PubErrorCustom("商品{}sku关联ID非法!".format(gdid))
            if not gd_sku_name:
                raise PubErrorCustom("商品{}sku关联名称非法!".format(gd_sku_name))

            try:
                obj = await self.db.get(Goods, gdid=gdid)
            except Goods.DoesNotExist:
                raise PubErrorCustom("商品{}不存在!".format(gdid))

            if obj.gd_status == '1':
                raise PubErrorCustom("商品{}已下架!".format(obj.gd_name))
            elif obj.gd_status == '2':
                raise PubErrorCustom("商品{}已售罄!".format(obj.gd_name))

