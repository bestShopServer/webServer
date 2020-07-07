

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

class SkuGroupRules:

    @staticmethod
    def post():
        return dict(
            robot={
                "pk_key": "group_id",
                "skugroup" : {
                    "form_class": SkuGroupForm,
                    "model_class": SkuGroup
                }
            }
        )

    @staticmethod
    def put():
        return dict(
            robot={
                "pk_key":"group_id",
                "skugroup": {
                    "form_class": SkuGroupForm,
                    "model_class": SkuGroup,
                    "father":True
                }
            }
        )

    @staticmethod
    def delete():
        return dict(
            robot={
                "pk_key": "group_id",
                "skugroup": {
                    "model_class": SkuGroup
                }
            }
        )

    @staticmethod
    def get():
        return dict(
            isTransaction=False,
            robot={
                "pk_key": "group_id",
                "skugroup": {
                    "model_class": SkuGroup,
                    "serializers":SkuGroupSerializer,
                    "page": True,
                    "query_params":[
                        {
                            "key":"userid",
                            "value":"user.userid",
                            "data_src":"data_pool",
                            "pool":"self"
                        }
                    ],
                    "child_form_link": {
                        "skuspecvalue": "spec_values"
                    },
                    "child": {
                        "skuspecvalue": {
                            "model_class": SkuSpecValue,
                        }
                    }
                }
            }
        )

class SkuSpecValueRules:

    @staticmethod
    def post():
        return dict(
            robot={
                "pk_key": "spec_id",
                "skuspecvalue" : {
                    "form_class": SkuSpecValueForm,
                    "model_class": SkuSpecValue
                }
            }
        )

    @staticmethod
    def put():
        return dict(
            robot={
                "pk_key":"spec_id",
                "skuspecvalue": {
                    "form_class": SkuSpecValueForm,
                    "model_class": SkuSpecValue,
                    "father":True
                }
            }
        )

    @staticmethod
    def delete():
        return dict(
            robot={
                "pk_key": "spec_id",
                "skuspecvalue": {
                    "model_class": SkuGroup
                }
            }
        )