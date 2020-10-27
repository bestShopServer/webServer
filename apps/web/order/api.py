
import json
from peewee import JOIN
from utils.database import MysqlPool
from apps.base import BaseHandler
from utils.decorator.connector import Core_connector
from utils.exceptions import PubErrorCustom
from router import route

from models.order import OrderList,Order,OrderDetail,OrderRefund
from models.user import User

from apps.web.order.serializers import OrderSerializerForOrder,OrderSerializerForOrderDetail

from loguru import logger

from apps.app.order.utils import PayBase

@route(None,id=True)
class order(BaseHandler):

    """
    订单管理
    """

    @Core_connector(isTransaction=False)
    async def get(self, pk=None):

        status = self.data.get("status", None)
        orderid = self.data.get("orderid",None)
        name = self.data.get("name",None)
        phone = self.data.get("phone", None)
        start_time = self.data.get("start_time", None)
        end_time = self.data.get("end_time",None)
        gd_name = self.data.get("gd_name",None)

        query = Order.select(Order,OrderDetail,User). \
                join(OrderDetail, join_type=JOIN.INNER, on=(OrderDetail.orderid == Order.orderid)). \
                join(User, join_type=JOIN.INNER, on=(User.userid == Order.userid)). \
                where(Order.super_userid == self.user.userid)

        if pk:
            query = query.where(Order.orderid == pk)

        else:
            if status and status != 'all':
                query = query.where(Order.status == status)

            if orderid :
                query = query.where(Order.orderid == orderid)

            if name:
                query = query.where(OrderDetail.name == name)

            if phone:
                query = query.where(OrderDetail.phone == phone)

            if start_time and end_time:
                query = query.where(Order.createtime >= start_time,Order.createtime<=end_time)

            query = query.paginate(self.data['page'], self.data['size'])
        row = await self.db.execute(query)
        count = len(row)

        orderids = [item.orderid for item in row]

        if len(orderids):

            orderlistQuery = OrderList.select().where(OrderList.orderid << orderids)

            if gd_name:
                orderlistQuery = orderlistQuery.where(OrderList.gd_name == gd_name)

            orderlistTmp = await self.db.execute(orderlistQuery)

            for item in row:
                for itemOrderlist in orderlistTmp:
                    if item.orderid == itemOrderlist.orderid:
                        if hasattr(item, "orderlist") and item.orderlist:
                            item.orderlist.append(itemOrderlist)
                        else:
                            item.orderlist = [itemOrderlist]

        if not pk:
            if len(orderids):
                orderRefundQuery = OrderRefund.select().where(OrderRefund.orderid << orderids)

                orderRefundTmp = await self.db.execute(orderRefundQuery)

                for item in row:
                    item.orderrefund = None
                    for itemOrderlist in orderRefundTmp:
                        if item.orderid == itemOrderlist.orderid:
                            item.orderrefund = itemOrderlist
                            break

            return {"data":OrderSerializerForOrder(row,many=True).data,"count":count}
        else:
            if len(row):
                row=row[0]
            else:
                raise PubErrorCustom("无此订单详情!")
            return {"data":OrderSerializerForOrderDetail(row,many=False).data,"count":count}

@route(None,id=True)
class order_refund_agree(BaseHandler):

    """
    订单退款同意
    """

    @Core_connector()
    async def put(self, pk=None):
        if not pk:
            raise PubErrorCustom("订单号不能为空!")

        obj = await self.db.execute(OrderRefund.select().for_update().where(OrderRefund.orderid == pk))

        if not len(obj):
            raise PubErrorCustom("退款信息{}不存在!".format(pk))
        else:
            obj = obj[0]

        if obj.status == '3':
            raise PubErrorCustom("退款单已拒绝,请勿非法操作!")
        elif obj.status == '1':
            raise PubErrorCustom("退款单正在退款,请勿操作!")
        elif obj.status == '2':
            raise PubErrorCustom("退款单退款成功,请勿非法操作!")

        await PayBase(
            app=self,
            trade={
                "out_trade_no": obj.orderid,
                "out_refund_no":obj.refund_id,
                "total_fee": int(obj.pay_amount * 100),
                "refund_fee":int(obj.refund_amount * 100),
                "method":"refund"
            }
        ).run()

        obj.status = '1'
        await self.db.update(obj)

@route()
class wechat_refund_callback(BaseHandler):
    """
    微信支付平台订单退款回调
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

@route(None,id=True)
class order_refund_reject(BaseHandler):

    """
    订单退款拒绝
    """

    @Core_connector()
    async def put(self, pk=None):
        if not pk:
            raise PubErrorCustom("订单号不能为空!")

        obj = await self.db.execute(OrderRefund.select().for_update().where(OrderRefund.orderid == pk))

        if not len(obj):
            raise PubErrorCustom("退款信息{}不存在!".format(pk))
        else:
            obj = obj[0]

        if obj.status == '2':
            raise PubErrorCustom("退款单已退款,请勿非法操作!")
        elif obj.status == '1':
            raise PubErrorCustom("退款单已拒绝,请勿重复操作!")

        obj.status = '3'
        await self.db.update(obj)