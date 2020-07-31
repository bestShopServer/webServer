

from apps.web.goods.forms import \
        GoodsCateGoryStyleForm,GoodsCateGoryForm,GoodsForm,\
            SkuGroupForm,SkuSpecValueForm

from apps.web.goods.serializers import \
        GoodsCateGoryStyleSerializer,GoodsCateGorySerializer,GoodsSerializer,\
            SkuGroupSerializer

from models.goods import \
    GoodsCateGoryStyle,GoodsCateGory,Goods,GoodsLinkSku,GoodsLinkCity,GoodsLinkCateGory,\
        SkuGroup,SkuSpecValue

from models.shop import ShopPage

from apps.web.shop.serializers import ShopPageDetailSerializer,ShopPageSerializer

from utils.time_st import UtilTime

class GoodsRules:

    @staticmethod
    def post():
        return dict(
            robot={
                "pk_key": "gdid",
                "goods" : {
                    "form_class": GoodsForm,
                    "model_class": Goods,
                    "father": True,
                    "child_form_link": {
                        "goodslinkcity": "gd_allow_area",
                        "goodslinkcategory":"gd_link_type",
                        "goodslinksku":"gd_sku_link"
                    },
                    "child": {
                        "goodslinkcity": {
                            "model_class": GoodsLinkCity,
                            "data_pool": {
                                "instance": {
                                    "userid": "userid",
                                    "gdid": "gdid"
                                }
                            }
                        },
                        "goodslinkcategory": {
                            "model_class": GoodsLinkCateGory,
                            "data_pool": {
                                "instance": {
                                    "userid": "userid",
                                    "gdid": "gdid"
                                }
                            }
                        },
                        "goodslinksku": {
                            "model_class": GoodsLinkSku,
                            "last_ids_key":"gd_sku_links",
                            "last_ids_level":1,
                            "sort_key":"sort",
                            "data_pool": {
                                "instance": {
                                    "userid": "userid",
                                    "gdid": "gdid"
                                }
                            }
                        },
                    }
                }
            }
        )

    @staticmethod
    def put():
        return dict(
            robot={
                "pk_key": "gdid",
                "goods": {
                    "form_class": GoodsForm,
                    "model_class": Goods,
                    "father":True,
                    "child_form_link": {
                        "goodslinkcity": "gd_allow_area",
                        "goodslinkcategory":"gd_link_type",
                        "goodslinksku": "gd_sku_link"
                    },
                    "child": {
                        "goodslinkcity": {
                            "model_class": GoodsLinkCity,
                            "data_pool": {
                                "instance": {
                                    "userid": "userid",
                                    "gdid": "gdid"
                                }
                            }
                        },
                        "goodslinkcategory": {
                            "model_class": GoodsLinkCateGory,
                            "data_pool": {
                                "instance": {
                                    "userid": "userid",
                                    "gdid": "gdid"
                                }
                            }
                        },
                        "goodslinksku": {
                            "model_class": GoodsLinkSku,
                            "last_ids_key": "gd_sku_links",
                            "last_ids_level": 1,
                            "data_pool": {
                                "instance": {
                                    "userid": "userid",
                                    "gdid": "gdid"
                                }
                            }
                        },
                    }
                }
            }
        )

    @staticmethod
    def delete():
        return dict(
            robot={
                "pk_key": "gdid",
                "goods": {
                    "model_class": Goods,
                    "child": {
                        "goodslinkcity": {
                            "model_class": GoodsLinkCity,
                        },
                        "goodslinkcategory": {
                            "model_class": GoodsLinkCateGory,
                        },
                        "goodslinksku": {
                            "model_class": GoodsLinkSku,
                        }
                    }
                }
            }
        )

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
                            "key":"userid",
                            "value":"user.userid",
                            "data_src":"data_pool",
                            "pool":"self"
                        },
                        {
                            "key": "gd_name",
                            "value": "data.gd_name",
                            "data_src": "data_pool",
                            "pool": "self"
                        },
                        {
                            "key": "gd_status",
                            "value": "data.gd_status",
                            "data_src": "data_pool",
                            "pool": "self"
                        },
                        {
                            "data_src": "data_pool",
                            "pool": "self",
                            "value":"data.start_datetime",
                            "value_format_func": lambda x:UtilTime().string_to_timestamp(x),
                            "query":{
                                "where": Goods.createtime.__ge__,
                            }
                        },
                        {
                            "data_src": "data_pool",
                            "pool": "self",
                            "value": "data.end_datetime",
                            "value_format_func": lambda x: UtilTime().string_to_timestamp(x),
                            "query": {
                                "where": Goods.createtime.__le__,
                            }
                        },
                        {
                            "key": "gdid",
                            "value": "data.gdcgids",
                            "data_src": "data_pool",
                            "pool": "self",
                            "query":{
                                "link_model_class":GoodsCateGory,
                                "where":GoodsCateGory.gdcgid.in_,
                                "last_where":Goods.gdid.in_
                            }
                        }
                    ]
                }
            }
        )

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
                            "key":"userid",
                            "value":"user.userid",
                            "data_src":"data_pool",
                            "pool":"self"
                        },
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
                    "model_class": SkuSpecValue
                }
            }
        )

class GoodsLinkShopPageRules:

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
                            "key": "gdid",
                            "value": "data.gdid",
                            "data_src": "data_pool",
                            "pool": "self"
                        },
                        {
                            "key": "type",
                            "value": "data.type",
                            "data_src": "data_pool",
                            "pool": "self",
                            "default":'1'
                        }
                    ]
                }
            }
        )