
from apps.base import BaseHandler

from utils.decorator.connector import Core_connector
from utils.exceptions import PubErrorCustom

from models.goods import GoodsCateGoryStyle,GoodsCateGory,Goods

from apps.app.public.serializers import GoodsCateGoryStyleForAppSerializer,GoodsCateGoryForAppSerializer,\
                GoodsByCateGoryForAppSerializer
from router import route

@route()
class goodscategorystyle(BaseHandler):

    """
    app获取分类样式
    """

    @Core_connector(isTicket=False)
    async def get(self):

        res = GoodsCateGoryStyleForAppSerializer(await self.db.execute(GoodsCateGoryStyle.select()), many=True).data
        return {"data":res[0] if res and len(res) else {}}

@route()
class goodscategory(BaseHandler):

    """
    app获取分类数据
    """

    @Core_connector(isTicket=False)
    async def get(self):

        return {"data": \
                    GoodsCateGoryForAppSerializer(
                        await self.db.execute(
                            GoodsCateGory.select().where(
                                GoodsCateGory.level == self.data.get("level",1),
                                GoodsCateGory.status == '0'
                            )
                        ), many=True).data}

# class goodsbycategory(BaseHandler):
#
#     """
#     app根据分类获取商品数据
#     """
#
#     @Core_connector(isTicket=False)
#     async def get(self):
#
#         level = self.data.get("level",1)
#         return {"data": \
#                     GoodsCateGoryForAppSerializer(
#                         await self.db.execute(
#                             GoodsCateGory.select().where(
#                                 GoodsCateGory.level==level
#                             )
#                         ), many=True).data}