

from models.shop import ShopPage
from apps.web.shop.forms import ShopPageForm
from apps.web.shop.serializers import ShopPageSerializer

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
                    "query_params":[
                        {
                            "key":"userid",
                            "value":"user.userid",
                            "data_src":"data_pool",
                            "pool":"self"
                        }
                    ]
                }
            }
        )