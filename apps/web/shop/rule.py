

from models.shop import ShopPage,ShopConfig
from apps.web.shop.forms import ShopPageForm,ShopConfigForm
from apps.web.shop.serializers import ShopPageSerializer,ShopPageDetailSerializer,ShopConfigSerializer

class ShopPageRules:

    @staticmethod
    def post():
        return dict(
            robot={
                "pk_key": "id",
                "shoppage" : {
                    "form_class": ShopPageForm,
                    "model_class": ShopPage,
                    "father": True
                }
            }
        )

    @staticmethod
    def put():
        return dict(
            robot={
                "pk_key": "id",
                "shoppage": {
                    "form_class": ShopPageForm,
                    "model_class": ShopPage,
                    "father": True
                }
            }
        )

    @staticmethod
    def delete():
        return dict(
            robot={
                "pk_key": "id",
                "shoppage": {
                    "model_class": ShopPage
                }
            }
        )

    @staticmethod
    def get():
        return dict(
            isTransaction=False,
            robot={
                "pk_key": "id",
                "shoppage": {
                    "model_class": ShopPage,
                    "page":True,
                    "serializers":ShopPageSerializer,
                    "detail_serializers":ShopPageDetailSerializer,
                    "sort": [ShopPage.type,ShopPage.createtime.desc()],
                    "query_params":[
                        {
                            "key":"userid",
                            "value":"user.userid",
                            "data_src":"data_pool",
                            "pool":"self"
                        },
                        {
                            "key": "type",
                            "value": "data.type",
                            "data_src": "data_pool",
                            "pool": "self",
                            "default":['0','9'],
                            "query":{
                                "where": ShopPage.type.in_,
                            }
                        }
                    ]
                }
            }
        )

class ShopConfigRules:

    @staticmethod
    def post():
        return dict(
            robot={
                "pk_key": "id",
                "shopconfig" : {
                    "form_class": ShopConfigForm,
                    "model_class": ShopConfig,
                    "father": True
                }
            }
        )

    @staticmethod
    def put():
        return dict(
            robot={
                "pk_key": "userid",
                "shopconfig": {
                    "form_class": ShopConfigForm,
                    "model_class": ShopConfig,
                    "father": True
                }
            }
        )

    @staticmethod
    def delete():
        return dict(
            robot={
                "pk_key": "userid",
                "shopconfig": {
                    "model_class": ShopConfig
                }
            }
        )

    @staticmethod
    def get():
        return dict(
            isTransaction=False,
            robot={
                "pk_key": "userid",
                "shopconfig": {
                    "model_class": ShopConfig,
                    "detail_serializers":ShopConfigSerializer,
                    "query_params": [
                        {
                            "key": "userid",
                            "value": "user.userid",
                            "data_src": "data_pool",
                            "pool": "self"
                        }
                    ]
                }
            }
        )