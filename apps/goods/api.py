

from apps.base import BaseHandler

from utils.decorator.connector import Core_connector
from utils.exceptions import PubErrorCustom
from models.goods import GoodsCateGory,Goods


class goodscategory(BaseHandler):

    @Core_connector()
    async def get(self, *args, **kwargs):
        pass

class goods(BaseHandler):

    @Core_connector()
    async def get(self, *args, **kwargs):
        pass