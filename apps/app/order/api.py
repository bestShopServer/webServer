
import json
from decimal import Decimal

from peewee import JOIN

from utils.database import MysqlPool

from apps.base import BaseHandler

from apps.app.order.serializers import OrderForAppSerializer,orderOrderDetailForAppSerializer

from utils.decorator.connector import Core_connector
from utils.exceptions import PubErrorCustom

from utils.time_st import UtilTime

from router import route

from apps.app.order.rule import AddressRules,ShopCartRules
from models.order import Address

from models.order import ShopCart,Order,OrderList,OrderDetail,OrderRefund
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
        shopcartObj.gd_number = int(number)

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

        if not address_id:
            raise PubErrorCustom("请填写收货地址!")

        orderid = await self.idGeneratorClass().ordercode()

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

            if obj.gd_specs_name_default_flag == '0':
                orderlistObj = await self.db.create(OrderList, **dict(
                    orderid=orderid,
                    gdid=obj.gdid,
                    gd_name=obj.gd_name,
                    gd_img=json.loads(obj.gd_banners)[0][1],
                    gd_price=obj.gd_show_price,
                    gd_item_no=obj.gd_item_no,
                    gd_weight=obj.gd_weight,
                    gd_unit=obj.gd_unit,
                    gd_sku_id=item['gd_sku_id'],
                    gd_sku_name=item['gd_sku_name'],
                    gd_number=item['gd_number']
                ))
            else:
                try:
                    skuObj = await self.db.get(GoodsLinkSku, id=item['gd_sku_id'])
                except GoodsLinkSku.DoesNotExist:
                    raise PubErrorCustom("SkuId{}不存在!".format(item['gd_sku_id']))

                orderlistObj = await self.db.create(OrderList, **dict(
                    orderid=orderid,
                    gdid=obj.gdid,
                    gd_img=skuObj.image,
                    gd_price=skuObj.price,
                    gd_name=obj.gd_name,
                    gd_item_no=skuObj.item_no,
                    gd_weight=skuObj.weight,
                    gd_unit=obj.gd_unit,
                    gd_sku_id=item['gd_sku_id'],
                    gd_sku_name=item['gd_sku_name'],
                    gd_number=item['gd_number']
                ))

            price += orderlistObj.gd_price * int(item['gd_number'])

        await self.db.create(Order, **dict(
            userid=self.user.userid,
            super_userid = 1, #先写死
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
            detail=address.address_detail
        ))

        return {"data":orderid}

@route()
class orderlist(BaseHandler):

    """
    订单列表查询
    """

    @Core_connector(isTransaction=False)
    async def get(self, pk=None):


        status = self.data.get("status",None)

        query = Order.select(Order).where(Order.userid == self.user.userid)

        if status and status!='all':
            query = query.where(Order.status == status)

        row = await self.db.execute(query)

        orderids = [item.orderid for item in row]

        if len(orderids):
            orderlistTmp = await self.db.execute(OrderList.select().where(OrderList.orderid << orderids))

            for item in row:
                for itemOrderlist in orderlistTmp:
                    if item.orderid == itemOrderlist.orderid:
                        if hasattr(item, "orderlist") and item.orderlist:
                            item.orderlist.append(itemOrderlist)
                        else:
                            item.orderlist = [itemOrderlist]

        return {"data": OrderForAppSerializer(row, many=True).data}

@route(None,id=True)
class orderdetail(BaseHandler):

    """
    订单详情查询
    """

    @Core_connector( isTransaction=False)
    async def get(self, pk=None):

        query = Order.select(Order, OrderDetail). \
            join(OrderDetail, join_type=JOIN.INNER, on=(OrderDetail.orderid == Order.orderid)). \
            where(Order.userid == self.user.userid)

        if pk:
            query = query.where(Order.orderid == pk)
        else:
            raise PubErrorCustom("请传入订单号!")

        row = await self.db.execute(query)

        orderids = [item.orderid for item in row]

        if len(orderids):
            orderlistTmp = await self.db.execute(OrderList.select().where(OrderList.orderid << orderids))

            for item in row:
                for itemOrderlist in orderlistTmp:
                    if item.orderid == itemOrderlist.orderid:
                        if hasattr(item, "orderlist") and item.orderlist:
                            item.orderlist.append(itemOrderlist)
                        else:
                            item.orderlist = [itemOrderlist]

        if len(orderids):
            orderRefundQuery = OrderRefund.select().where(OrderRefund.orderid << orderids)

            orderRefundTmp = await self.db.execute(orderRefundQuery)

            for item in row:
                item.orderrefund = None
                for itemOrderlist in orderRefundTmp:
                    if item.orderid == itemOrderlist.orderid:
                        item.orderrefund = itemOrderlist
                        break

        if len(row):
            row = row[0]
        return {"data": orderOrderDetailForAppSerializer(row, many=False).data}


@route()
class ordercount(BaseHandler):

    """
    订单数目查询
    """

    @Core_connector(isTransaction=False)
    async def get(self, pk=None):

        r_data={
            "dfk":0,
            "dfh":0,
            "dsh":0,
            "tkz":0
        }

        for item in await self.db.execute(Order.select(Order).where(Order.userid == self.user.userid)):
            if item.status == '0':
                r_data['dfk'] += 1
            elif item.status == '1':
                r_data['dfh'] += 1
            elif item.status == '2':
                r_data['dsh'] += 1
            elif item.status == '6':
                r_data['tkz'] += 1

        return {"data":r_data}

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
        except OrderDetail.DoesNotExist:
            raise PubErrorCustom("订单{}不存在!".format(pk))

        orderdetail.pay_type = paytype
        await self.db.update(orderdetail)

        amount = order.pay_amount  #单位元,实际支付金额

        return {"data":await PayBase(
            app=self,
            trade={
                "out_trade_no":order.orderid,
                "total_fee" : int(amount * 100),
                "openid":self.user.uuid,
                "spbill_create_ip":self.request.remote_ip,
                "paytype":paytype,
                "method":"create"
            }
        ).run()}


@route(None,id=True)
class order_refund_apply(BaseHandler):
    """
    订单退款申请
    """

    @Core_connector()
    async def put(self, pk=None):
        if not pk:
            raise PubErrorCustom("订单号不能为空!")

        try:
            await self.db.get(OrderRefund, orderid=pk)
            raise PubErrorCustom("已申请退款!")
        except OrderRefund.DoesNotExist:
            pass

        order = await self.db.execute(Order.select().for_update().where(Order.orderid == pk))
        if not len(order):
            raise PubErrorCustom("订单{}不存在!".format(pk))
        else:
            order = order[0]

        order.status = '6'
        order.status_list = json.dumps(json.loads(order.status_list).append({"status": "6", "time": UtilTime().timestamp}))

        refundObj = await self.db.create(OrderRefund, **dict(
            orderid=order.orderid,
            refund_id = await self.idGeneratorClass().ordercode(),
            status = '0',
            pay_amount = order.pay_amount,
            refund_amount = order.pay_amount
        ))

        await self.db.update(order)

        return {"data": refundObj.orderid}


@route()
class wechat_callback(BaseHandler):
    """
    微信支付平台订单回调
    """

    async def post(self, *args, **kwargs):

        msg = self.request.body.decode('utf-8')
        logger.info("微信回调数据=>{}".format(msg))
        self.set_header("Content-Type", "text/xml; charset=UTF-8")
        try:
            async with MysqlPool().get_conn.atomic_async():
                await PayBase(
                    app=self,
                    trade={
                        "method": "callback",
                        "paytype":'0',
                        "callback_msg":msg
                    }
                ).run()
            await self.finish("""<xml><return_code><![CDATA[SUCCESS]]></return_code>
                            <return_msg><![CDATA[OK]]></return_msg></xml>""")
        except Exception:
            await self.finish("""<xml><return_code><![CDATA[FAIL]]></return_code>                          
                                    <return_msg><![CDATA[Signature_Error]]></return_msg></xml>""")

