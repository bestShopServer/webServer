
from models.goods import Goods,GoodsCateGory
from apps.web.goods.serializers import GoodsSerializer
from peewee import JOIN


class GoodsbyidsRules:

    @staticmethod
    def get():
        return dict(
            isTransaction=False,
            robot={
                "pk_key": "gdid",
                "goods": {
                    "model_class": Goods,
                    "serializers":GoodsSerializer,
                    "page": True,
                    "query_params":[
                        {
                            "value": "data.gdids",
                            "data_src": "data_pool",
                            "pool": "self",
                            "query":{
                                "where":Goods.gdid.in_,
                            }
                        }
                    ]
                }
            }
        )

class GoodsbyCateGoryRules:

    @staticmethod
    def get():
        return dict(
            isTransaction=False,
            robot={
                "pk_key": "gdid",
                "goods": {
                    "model_class": Goods,
                    "serializers":GoodsSerializer,
                    "page": True,
                    "query_params":[
                        {
                            "key": "gdid",
                            "value": "data.gdcgid",
                            "data_src": "data_pool",
                            "pool": "self",
                            "query":{
                                "link_model_class":GoodsCateGory,
                                "key":"gdcgid",
                                "last_where":Goods.gdid.in_,
                            }
                        }
                    ]
                }
            }
        )