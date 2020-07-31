
from apps.base import BaseHandler

from utils.decorator.connector import Core_connector
from utils.exceptions import PubErrorCustom

from models.goods import GoodsCateGoryStyle,GoodsCateGory,Goods

from apps.app.public.serializers import GoodsCateGoryStyleForAppSerializer,GoodsCateGoryForAppSerializer,\
                GoodsByCateGoryForAppSerializer
from router import route

from apps.app.goods.rule import GoodsbyidsRules,GoodsbyCateGoryRules

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
                                GoodsCateGory.gdcglastid == 0,
                                GoodsCateGory.status == '0'
                            )
                        ), many=True).data}


@route()
class goodscategorybygdcglastid(BaseHandler):

    @Core_connector(isTicket=False)
    async def get(self):

        if not self.data.get("gdcglastid",None):
            raise PubErrorCustom("上级ID不能为空!")

        async def recursion(gdcglastid):

            res = await self.db.execute(
                GoodsCateGory.select().where(
                    GoodsCateGory.gdcglastid == gdcglastid,
                    GoodsCateGory.status == '0'
                ).order_by(GoodsCateGory.sort)
            )

            child = GoodsCateGoryForAppSerializer(res, many=True).data

            if not len(child):
                return

            for item in child:
                item['child'] = await recursion(item['gdcgid'])

            return child

        return {"data":await recursion(gdcglastid=self.data['gdcglastid'])}

@route()
class goodsbyids(BaseHandler):
    @Core_connector(**{**GoodsbyidsRules.get(),**{"isTicket":False}})
    async def get(self, pk=None):
        pass

@route()
class goodsbycategory(BaseHandler):
    @Core_connector(**{**GoodsbyCateGoryRules.get(),**{"isTicket":False}})
    async def get(self, pk=None):
        pass


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