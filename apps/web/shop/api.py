import json

from loguru import logger
from apps.base import BaseHandler

from utils.decorator.connector import Core_connector
from utils.exceptions import PubErrorCustom

from models.user import User

from apps.web.shop.rule import ShopPageRules,ShopConfigRules

from models.shop import ShopPage

from router import route


@route(None,id=True)
class baseinfo(BaseHandler):
    """
    店铺基础信息
    """

    @Core_connector()
    async def post(self):

        try:
            obj = await self.db.get(User,userid=self.user.userid)
        except User.DoesNotExist:
            raise PubErrorCustom("拒绝访问!")

        shopinfo = json.loads(obj.shopinfo)
        shopinfo['shopname'] = self.data.get("shopname","")
        shopinfo['goodscategory_level'] = self.data.get("goodscategory_level", 0)
        shopinfo['wechat']['appid'] = self.data.get("appid","")
        shopinfo['wechat']['secret'] = self.data.get("secret", "")
        shopinfo['wechat']['pay_mchid'] = self.data.get("pay_mchid", "")
        shopinfo['wechat']['pay_key'] = self.data.get("pay_key", "")

        obj.shopinfo = json.dumps(shopinfo)
        await self.db.update(obj)

        return None

    @Core_connector()
    async def get(self):

        try:
            obj = await self.db.get(User,userid=self.user.userid)
        except User.DoesNotExist:
            raise PubErrorCustom("拒绝访问!")

        shopinfo = json.loads(obj.shopinfo)
        return {"data":{
            "shopname" : shopinfo['shopname'],
            "goodscategory_level": shopinfo['goodscategory_level'],
            "appid": shopinfo['wechat']['appid'],
            "secret": shopinfo['wechat']['secret'],
            "pay_mchid": shopinfo['wechat']['pay_mchid'],
            "pay_key": shopinfo['wechat']['pay_key']
        }}

@route(None,id=True)
class shoppage(BaseHandler):
    """
    微页面
    """

    @Core_connector(**ShopPageRules.post())
    async def post(self, *args, **kwargs):
        return {"data":self.pk}

    @Core_connector(**ShopPageRules.put())
    async def put(self, *args, **kwargs):
        return {"data":self.pk}

    @Core_connector(**ShopPageRules.delete())
    async def delete(self, *args, **kwargs):
        pass

    @Core_connector(**ShopPageRules.get())
    async def get(self, *args, **kwargs):
        pass

@route(None,id=True)
class shoppagetype(BaseHandler):

    @Core_connector()
    async def put(self, pk=None):

        type = self.data.get("type",None)
        if not type:
            raise PubErrorCustom("类型不能为空!!")

        logger.info("pk=>{}".format(pk))

        if type == '0':
            for item in await self.db.execute(\
                    ShopPage.select().for_update().\
                            where(ShopPage.userid==self.user.userid,ShopPage.type << ['0','9'])):
                if int(pk) == item.id:
                    item.type = type
                else:
                    item.type = '9'
                await self.db.update(item)

@route(None,id=True)
class shopconfig(BaseHandler):
    """
    店铺基础配置
    """

    @Core_connector(**ShopConfigRules.post())
    async def post(self, *args, **kwargs):
        pass

    @Core_connector(**ShopConfigRules.put())
    async def put(self, *args, **kwargs):
        pass

    @Core_connector(**ShopConfigRules.delete())
    async def delete(self, *args, **kwargs):
        pass

    @Core_connector(**ShopConfigRules.get())
    async def get(self, *args, **kwargs):
        pass