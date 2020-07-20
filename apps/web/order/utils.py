

from peewee import JOIN

from utils.exceptions import PubErrorCustom
from models.order import Order,OrderList,OrderDetail

class OrderBase(object):

    def __init__(self,**kwargs):

        self.orderid = kwargs.get("orderid",None)
        self.db = kwargs.get("db",None)

    async def get(self):

        try:
            self.order = await self.db.get(Order,orderid=self.orderid)
        except Order.DoesNotExist:
            raise PubErrorCustom("{}订单号不存在!".format(self.orderid))

    async def create(self):
        pass


class OrderQueryBase(object):

    def __init__(self,**kwargs):

        self.db = kwargs.get("db",None)

    async def get(self,**kwargs):

        userid = kwargs.get("userid",None)
        orderid = kwargs.get("orderid",None)
        trade_no = kwargs.get("trade_no",None)

        start_time = kwargs.get("start_time",None)
        end_time = kwargs.get("end_time",None)

        gd_name = kwargs.get("gd_name",None)

        query = Order.select(Order,OrderDetail,OrderList). \
            join(OrderDetail, join_type=JOIN.INNER, on=(OrderDetail.orderid == Order.orderid)). \
            join(OrderList, join_type=JOIN.INNER, on=(OrderList.orderid == Order.orderid)). \
            where(Order.userid == userid)

        if orderid:
            query = query.where(Order.orderid == orderid)

        if trade_no:
            query = query.where(Order.trade_no == trade_no)

        if start_time:
            query = query.where(Order.createtime >= start_time)

        if end_time:
            query = query.where(Order.createtime <= end_time)

        if gd_name:
            query = query.where(OrderList.gd_name == gd_name)







