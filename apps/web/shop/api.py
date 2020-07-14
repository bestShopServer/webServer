import json

from apps.base import BaseHandler

from utils.decorator.connector import Core_connector
from utils.exceptions import PubErrorCustom

from models.user import User

from apps.web.shop.rule import ShopPageRules,ShopConfigRules

class baseinfo(BaseHandler):
    """
    店铺基础信息
    """

    @Core_connector()
    async def post(self):

        try:
            obj = await self.db.get(User,userid=self.user['userid'])
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
            obj = await self.db.get(User,userid=self.user['userid'])
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

class shoppage(BaseHandler):
    """
    微页面
    """

    @Core_connector(**ShopPageRules.post())
    async def post(self, *args, **kwargs):
        pass

    @Core_connector(**ShopPageRules.put())
    async def put(self, *args, **kwargs):
        pass

    @Core_connector(**ShopPageRules.delete())
    async def delete(self, *args, **kwargs):
        pass

    @Core_connector(**ShopPageRules.get())
    async def get(self, *args, **kwargs):
        pass


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