

from apps.app.order.forms import AddressForm
from models.order import Address
from apps.app.order.serializers import AddressForAppSerializer

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
                    ],
                }
            }
        )