

from apps.base import BaseHandler

from utils.decorator.connector import Core_connector
from utils.exceptions import PubErrorCustom

from models.shop import ShopPage,ShopConfig

from apps.app.public.serializers import ShopPageForAppSerializer,ShopConfigForAppSerializer
from router import route

@route()
class baseinfo(BaseHandler):

    """
    app获取基础信息
    """

    @Core_connector(isTicket=False)
    async def get(self):

        data={
            "indexPage":{},
            "menuData":{}
        }

        #获取首页模板数据
        res = ShopPageForAppSerializer(await self.db.execute(ShopPage.select().where(ShopPage.type == '0')),many=True).data
        data['indexPage'] = res[0] if res and len(res) else {}

        #获取菜单数据
        res = ShopConfigForAppSerializer(await self.db.execute(ShopConfig.select()),many=True).data
        data['menuData'] = res[0] if res and len(res) else {}

        return {"data":data}



