

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
                    "unique": [
                        {
                            "key": "userid",
                            "value": "user.userid",
                            "data_src": "data_pool",
                            "pool": "self"
                        }
                    ],
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
                "goodscategorystyle": {
                    "page": True,
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

class GoodsCateGoryRules:

    @staticmethod
    def post():
        return dict(
            robot={
                "pk_key": "gdcgid",
                "goodscategory" : {
                    "form_class": GoodsCateGoryForm,
                    "model_class": GoodsCateGory
                }
            }
        )

    @staticmethod
    def put():
        return dict(
            robot={
                "pk_key":"gdcgid",
                "goodscategory": {
                    "form_class": GoodsCateGoryForm,
                    "model_class": GoodsCateGory,
                    "father":True
                }
            }
        )

    @staticmethod
    def delete():
        return dict(
            robot={
                "pk_key": "gdcgid",
                "goodscategory": {
                    "model_class": GoodsCateGory
                }
            }
        )

    @staticmethod
    def get():
        return dict(
            isTransaction=False,
            robot={
                "pk_key": "gdcgid",
                "goodscategory": {
                    "model_class": GoodsCateGory,
                    "serializers":GoodsCateGorySerializer,
                    "sort":GoodsCateGory.sort,
                    "query_params":[
                        {
                            "key":"userid",
                            "value":"user.userid",
                            "data_src":"data_pool",
                            "pool":"self"
                        },
                        {
                            "key":"gdcglastid",
                            "value": "data.gdcglastid",
                            "data_src":"data_pool",
                            "pool":"self"
                        }
                    ],
                }
            }
        )