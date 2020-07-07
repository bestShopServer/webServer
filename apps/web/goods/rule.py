

from apps.web.goods.forms import \
        GoodsCateGoryStyleForm,GoodsCateGoryForm,GoodsForm,\
            SkuGroupForm,SkuSpecValueForm

from apps.web.goods.serializers import \
        GoodsCateGoryStyleSerializer,GoodsCateGorySerializer,GoodsSerializer,GoodsDetailSerializer,\
            SkuGroupSerializer

from models.goods import \
    GoodsCateGoryStyle,GoodsCateGory,Goods,GoodsLinkSku,GoodsLinkCity,GoodsLinkCateGory,\
        SkuGroup,SkuSpecValue

class GoodsCateGoryStyleRules:

    @staticmethod
    def post():
        return dict(
            robot={
                "pk_key": "id",
                "goodscategorystyle" : {
                    "unique": [
                        {
                            "key":"userid",
                            "value":"user.userid",
                            "data_src":"data_pool",
                            "pool":"self"
                        }
                    ],
                    "form_class": GoodsCateGoryStyleForm,
                    "model_class": GoodsCateGoryStyle
                }
            }
        )

    @staticmethod
    def put():
        return dict(
            robot={
                "pk_key":"id",
                "goodscategorystyle": {
                    "form_class": GoodsCateGoryStyleForm,
                    "model_class": GoodsCateGoryStyle,
                    "father":True
                }
            }
        )

    @staticmethod
    def delete():
        return dict(
            robot={
                "pk_key": "id",
                "goodscategorystyle": {
                    "model_class": GoodsCateGoryStyle
                }
            }
        )

    @staticmethod
    def get():
        return dict(
            isTransaction=False,
            robot={
                "pk_key": "id",
                "page":True,
                "goodscategorystyle": {
                    "model_class": GoodsCateGoryStyle,
                    "serializers":GoodsCateGoryStyleSerializer,
                    "query_params":[
                        {
                            "key":"userid",
                            "value":"user.userid",
                            "data_src":"data_pool",
                            "pool":"self"
                        }
                    ],
                }
            }
        )