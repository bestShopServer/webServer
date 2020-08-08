

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

    async def get_before_handler(self,**kwargs):

        self.data['detail'] = True

    @Core_connector(**{**ShopPageRules.get(),**{"get_before_handler":get_before_handler,"isTicket":False}})
    async def get(self, *args, **kwargs):
        pass