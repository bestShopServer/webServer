
import json
from peewee import JOIN
from apps.base import BaseHandler
from utils.decorator.connector import Core_connector
from utils.exceptions import PubErrorCustom
from router import route

from models.order import OrderList,Order,OrderDetail
from models.user import User

from apps.web.order.serializers import OrderSerializerForOrder



@route(None,id=True)
class order(BaseHandler):

    """
    订单管理
    """

    @Core_connector(isTransaction=False)
    async def get(self, pk=None):

        status = self.data.get("status", None)
        orderid = self.data.get("userid",None)
        name = self.data.get("name",None)
        phone = self.data.get("phone", None)
        start_time = self.data.get("start_time", None)
        end_time = self.data.get("end_time",None)
        gd_name = self.data.get("gd_name",None)

        query = Order.select(Order,OrderDetail,User). \
                join(OrderDetail, join_type=JOIN.INNER, on=(OrderDetail.orderid == Order.orderid)). \
                join(User, join_type=JOIN.INNER, on=(User.userid == Order.userid)). \
                where(Order.super_userid == self.user.userid)

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

        row = await self.db.execute(query)

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

        return {"data":OrderSerializerForOrder(row,many=True).data}