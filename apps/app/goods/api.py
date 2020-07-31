
from apps.base import BaseHandler

from utils.decorator.connector import Core_connector
from utils.exceptions import PubErrorCustom

from models.goods import GoodsCateGoryStyle,GoodsCateGory,Goods

from apps.app.public.serializers import GoodsCateGoryStyleForAppSerializer,GoodsCateGoryForAppSerializer,\
                GoodsByCateGoryForAppSerializer
from router import route

from apps.app.goods.rule import GoodsbyidsRules,GoodsbyCateGoryRules
from apps.web.goods.serializers import GoodsSerializer

from loguru import logger

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

@route()
class goodslist(BaseHandler):
    @Core_connector(isTicket=False)
    async def get(self, pk=None):

        gd_name = self.data.get("gd_name",None)

        sort_key = self.data.get("sort_key",None)
        sort = self.data.get("sort",False)

        query = Goods.select()

        if gd_name:
            query = query.where(Goods.gd_name % '%{}%'.format(gd_name))

        if sort_key:
            if sort:
                query = query.order_by(getattr(Goods,sort_key))
            else:
                query = query.order_by(getattr(Goods, sort_key).desc())

        # count = len(await self.db.execute(query))
        query = query.paginate(self.data['page'], self.data['size'])

        logger.info(query)

        resposne = await self.db.execute(query)

        return {
            "data": GoodsSerializer(resposne,many=True).data,
            # "count": count
        }



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