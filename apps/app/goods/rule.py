
from models.goods import Goods
from apps.web.goods.serializers import GoodsSerializer


class GoodsbyidsRules:

    @staticmethod
    def get():
        return dict(
            isTransaction=False,
            robot={
                "pk_key": "gdcgid",
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