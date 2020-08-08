

from apps.base import BaseHandler

from utils.decorator.connector import Core_connector
from utils.exceptions import PubErrorCustom
from router import route
from apps.web.shop.rule import ShopPageRules


@route(None,id=True)
class shoppage(BaseHandler):
    """
    微页面
    """

    @Core_connector(**ShopPageRules.get())
    async def get(self, *args, **kwargs):
        pass