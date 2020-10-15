
import json
from decimal import Decimal

from utils.database import MysqlPool

from apps.base import BaseHandler

from utils.decorator.connector import Core_connector
from utils.exceptions import PubErrorCustom

from utils.time_st import UtilTime

from router import route

from apps.app.order.rule import AddressRules,ShopCartRules
from models.order import Address

from models.order import ShopCart,Order,OrderList,OrderDetail
from models.goods import Goods,GoodsLinkSku

from apps.app.order.utils import PayBase

from loguru import logger

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

        number = self.data.get("number", None)

        shopcartObj = await self.db.execute(ShopCart.select().for_update().where(ShopCart.id == pk))

        logger.info(shopcartObj)

        if not len(shopcartObj):
            raise PubErrorCustom("无此数据")

        shopcartObj = shopcartObj[0]
        shopcartObj.gd_number += int(number)

        await self.db.update(shopcartObj)

    @Core_connector(**ShopCartRules().delete())
    async def delete(self, *args, **kwargs):
        pass

    @Core_connector(**ShopCartRules().get())
    async def get(self, pk=None):
        pass

@route()
class order(BaseHandler):

    """
    生成订单
    """

    @Core_connector()
    async def post(self, *args, **kwargs):

        shopcarts = self.data.get("shopcarts", [])
        memo = self.data.get("memo","")
        address_id = self.data.get("address_id",None)

        if not len(shopcarts):
            raise PubErrorCustom("请选择购买的商品!")

        if not len(address_id):
            raise PubErrorCustom("请填写收货地址!")

        orderid = await self.idGeneratorClass.ordercode()

        price = Decimal(0.0)

        for item in shopcarts:

            try:
                obj = await self.db.get(Goods, gdid=item['gdid'])
            except Goods.DoesNotExist:
                raise PubErrorCustom("商品{}不存在!".format(item['gdid']))

            if obj.gd_status == '1':
                raise PubErrorCustom("商品{}已下架!".format(obj.gd_name))
            elif obj.gd_status == '2':
                raise PubErrorCustom("商品{}已售罄!".format(obj.gd_name))

            await self.db.create(OrderList, **dict(
                orderid=orderid,
                gdid=obj.gdid,
                gd_img=json.loads(obj.gd_banners)[0][1],
                gd_price=item['gd_price'],
                gd_number=item['gd_number'],
                gd_item_no=item['gd_item_no'],
                gd_weight=item['gd_weight'],
                gd_sku_id=item['gd_sku_id'],
                gd_sku_name=item['gd_sku_name'],
                gd_unit=item['gd_unit']
            ))

            price += Decimal(str(item['gd_price']) * int(item['gd_number']))

        await self.db.create(Order, **dict(
            userid=self.user.userid,
            orderid=orderid,
            status='0',
            status_list=json.dumps([{"status": "0", "time": UtilTime().timestamp}]),
            price=price,
            pay_amount=price,
            fare_amount=Decimal('0.00')
        ))

        try:
            address = await self.db.get(Address, id=address_id)
        except Goods.DoesNotExist:
            raise PubErrorCustom("收货地址{}不存在!".format(address_id))

        await self.db.create(OrderDetail, **dict(
            orderid=orderid,
            memo=memo,
            name=address.name,
            phone=address.mobile,
            province_code=address.province_code,
            province_name=address.province_name,
            city_code=address.city_code,
            city_name=address.city_name,
            county_code=address.county_code,
            county_name=address.county_name,
            detail=address.detail
        ))

        return {"data":orderid}


@route(None,id=True)
class orderpay(BaseHandler):
    """
    订单支付
    """

    @Core_connector()
    async def put(self, pk=None):
        if not pk:
            raise PubErrorCustom("id不能为空!")

        paytype = self.data.get("paytype",None)

        if not len(paytype):
            raise PubErrorCustom("请选择支付方式!")

        try:
            order = await self.db.get(Order, orderid=pk)
        except Order.DoesNotExist:
            raise PubErrorCustom("订单{}不存在!".format(pk))

        try:
            orderdetail = await self.db.get(OrderDetail, orderid=pk)
        except Order.DoesNotExist:
            raise PubErrorCustom("订单{}不存在!".format(pk))

        orderdetail.pay_type = paytype
        await self.db.update(orderdetail)

        amount = order.pay_amount  #单位元,实际支付金额

        return {"data":await PayBase(
            app=self,
            trade={
                "appid":"wx2c4649a77ef8edcd",
                "mch_id":"1514182671",
                "out_trade_no":order.orderid,
                "total_fee" : int(amount * 100),
                "openid":self.user.uuid,
                "pay_key":"15176427685562895401199204202038",
                "spbill_create_ip":self.request.remote_ip,
                "paytype":paytype,
                "method":"create"
            }
        ).run()}

@route()
class wechat_callback(BaseHandler):
    """
    微信支付平台订单回调
    """

    async def post(self, *args, **kwargs):

        self.set_header("Content-Type", "text/xml; charset=UTF-8")
        try:
            async with MysqlPool().get_conn.atomic_async():
                await PayBase(
                    app=self,
                    trade={
                        "pay_key": "15176427685562895401199204202038",
                        "method": "callback",
                        "paytype":'0'
                    }
                ).run()
            self.finish("""<xml><return_code><![CDATA[SUCCESS]]></return_code>
                            <return_msg><![CDATA[OK]]></return_msg></xml>""")
        except Exception:
            self.finish("""<xml><return_code><![CDATA[FAIL]]></return_code>                          
                                    <return_msg><![CDATA[Signature_Error]]></return_msg></xml>""")