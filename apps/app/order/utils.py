

from models.order import ShopCart
from models.goods import Goods



class ShopCartBase(object):

    def __init__(self,**kwargs):

        self.app = kwargs.get("app")


    