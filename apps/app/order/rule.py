

from apps.app.order.forms import AddressForm
from models.order import Address,ShopCart
from apps.app.order.serializers import AddressForAppSerializer,ShopCartForAppSerializer

class AddressRules:

    @staticmethod
    def post():
        return dict(
            robot={
                "pk_key": "id",
                "address" : {
                    "form_class": AddressForm,
                    "model_class": Address
                }
            }
        )

    @staticmethod
    def put():
        return dict(
            robot={
                "pk_key":"id",
                "address": {
                    "form_class": AddressForm,
                    "model_class": Address,
                    "father":True
                }
            }
        )

    @staticmethod
    def delete():
        return dict(
            robot={
                "pk_key": "id",
                "address": {
                    "model_class": Address
                }
            }
        )

    @staticmethod
    def get():
        return dict(
            isTransaction=False,
            robot={
                "pk_key": "id",
                "address": {
                    "model_class": Address,
                    "page":True,
                    "serializers":AddressForAppSerializer,
                    "query_params":[
                        {
                            "key":"userid",
                            "value":"user.userid",
                            "data_src":"data_pool",
                            "pool":"self"
                        },
                        {
                            "key": "address_default",
                            "value": "data.address_default",
                            "data_src": "data_pool",
                            "pool": "self"
                        },
                    ],
                }
            }
        )

class ShopCartRules:


    @staticmethod
    def delete():
        return dict(
            robot={
                "pk_key": "id",
                "shopcart": {
                    "model_class": ShopCart
                }
            }
        )

    @staticmethod
    def get():
        return dict(
            isTransaction=False,
            robot={
                "pk_key": "id",
                "shopcart": {
                    "model_class": ShopCart,
                    "page":True,
                    "serializers":ShopCartForAppSerializer,
                    "query_params":[
                        {
                            "key":"userid",
                            "value":"user.userid",
                            "data_src":"data_pool",
                            "pool":"self"
                        },
                    ],
                }
            }
        )