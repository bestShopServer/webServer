
import json
from apps.base import BaseHandler

from utils.decorator.connector import Core_connector
from utils.exceptions import PubErrorCustom

from router import route

from apps.app.order.rule import AddressRules,ShopCartRules
from models.order import Address

from models.order import ShopCart
from models.goods import Goods,GoodsLinkSku

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

        number = self.data.get("number", None)
        gdid = self.data.get("gdid", None)
        gd_sku_id = self.data.get("gd_sku_id", None)
        gd_sku_name = self.data.get("gd_sku_name", None)

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


        if gd_sku_id>0:
            try:
                skuObj = await self.db.get(GoodsLinkSku, id=gd_sku_id)
            except GoodsLinkSku.DoesNotExist:
                raise PubErrorCustom("商品{}关联SKU不存在!".format(gdid))
            gd_img = skuObj.image
            gd_price = skuObj.price
            gd_item_no = skuObj.item_no
            gd_weight = skuObj.weight
        else:
            gd_img = json.loads(obj.gd_banners)[0]
            gd_price = obj.gd_show_price
            gd_item_no = obj.gd_item_no
            gd_weight = obj.gd_weight

        try:
            shopcartObj = await  self.db.get(ShopCart,**dict(
                userid=self.user.userid,
                gdid=gdid,
                gd_sku_id=gd_sku_id
            ))
            shopcartObj.gd_number += number
            await self.db.execute(shopcartObj)
        except ShopCart.DoesNotExist:
            await self.db.create(ShopCart,**dict(
                userid=self.user.userid,
                gdid=gdid,
                gd_sku_id=gd_sku_id,
                gd_img=gd_img,
                gd_name=obj.gd_name,
                gd_price=gd_price,
                gd_number=number,
                gd_item_no=gd_item_no,
                gd_sku_name=gd_sku_name,
                gd_unit=obj.gd_unit,
                gd_weight=gd_weight
            ))

    @Core_connector()
    async def put(self, pk=None):
        if not pk:
            raise PubErrorCustom("id不能为空!")

        operation = self.data.get("operation","+")

        shopcartObj = await self.db.execute(ShopCart.select().for_update().where(ShopCart.id == pk))

        if not len(shopcartObj):
            raise PubErrorCustom("无此数据")

        shopcartObj = shopcartObj[0]
        if operation == '+':
            shopcartObj.gd_number += 1
        else:
            shopcartObj.gd_number -= 1
        await self.db.execute(shopcartObj)

    @Core_connector(**ShopCartRules().delete())
    async def delete(self, *args, **kwargs):
        pass

    @Core_connector(**ShopCartRules().get())
    async def get(self, pk=None):
        pass