
from models.shop import ShopPage
from apps.app.shop.serializers import ShopPageDetailForAppSerializer


class ShopPageRules:

    @staticmethod
    def get():
        return dict(
            isTransaction=False,
            robot={
                "pk_key": "id",
                "shoppage": {
                    "model_class": ShopPage,
                    "page":True,
                    "detail_serializers":ShopPageDetailForAppSerializer
                }
            }
        )