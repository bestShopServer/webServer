

from apps.base import BaseHandler

from utils.decorator.connector import Core_connector
from utils.exceptions import PubErrorCustom

from models.shop import ShopPage,ShopConfig

from apps.app.public.serializers import ShopPageForAppSerializer,ShopConfigForAppSerializer
from router import route

from data.base import datacity

@route()
class index(BaseHandler):

    """
    app获取首页信息
    """

    @Core_connector(isTicket=False)
    async def get(self):

        #获取首页模板数据
        res = ShopPageForAppSerializer(await self.db.execute(ShopPage.select().where(ShopPage.type == '0')),many=True).data
        indexPage = res[0] if res and len(res) else {}

        return {"data":indexPage}

@route()
class menu(BaseHandler):

    """
    app获取菜单信息
    """

    @Core_connector(isTicket=False)
    async def get(self):

        #获取菜单数据
        res = ShopConfigForAppSerializer(await self.db.execute(ShopConfig.select()),many=True).data
        menuData = res[0] if res and len(res) else {}

        return {"data":menuData}


@route(None,id=True)
class citycode(BaseHandler):
    @Core_connector(isTransaction=False,is_query_standard=False)
    async def get(self, pk=None):
        return {"data": await datacity(redis=self.redis).get()}
