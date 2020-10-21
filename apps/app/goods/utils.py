

from models.goods import Goods,GoodsLinkSku
from utils.exceptions import PubErrorCustom
from decimal import Decimal

class GoodsBase(object):

    def __init__(self,**kwargs):

        self.app = kwargs.get("app")

    #根据商品Sku id获取信息
    async def getGoodsForSkuid(self,gd_sku_id=None):

        pass

    #根据商品ID获取商品信息
    #暂时没空写
    async def getGoodsForGdid(self,gdid=None):

        try:
            goods = await self.app.db.get(Goods, gdid=gdid)
        except Goods.DoesNotExist:
            raise PubErrorCustom("商品{}不存在!".format(gdid))

        if goods.gd_specs_name_default_flag == '0':

            r_goods={
                "gd_show_price":goods.gd_show_price,
                "gd_stock_tot":goods.gd_stock_tot,
                "gd_specs_name_default":goods.gd_specs_name_default,
                "gd_item_no":goods.gd_item_no,
                "gd_weight": goods.gd_weight,
                "gd_status":goods.gd_status,
                "gd_item_no": goods.gd_item_no,
                "gd_item_no": goods.gd_item_no,
            }
        else:
            pass


