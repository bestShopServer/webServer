

from models.shop import ShopPage
from apps.web.shop.forms import ShopPageForm
from apps.web.shop.serializers import ShopPageSerializer,ShopPageDetailSerializer

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