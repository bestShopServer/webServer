
import json
from decimal import Decimal
from rest_framework import serializers
from utils.time_st import UtilTime

class GoodsCateGoryStyleForAppSerializer(serializers.Serializer):

    typecode = serializers.CharField()
    type = serializers.CharField()

class GoodsCateGoryForAppSerializer(serializers.Serializer):

    gdcgid = serializers.IntegerField()
    gdcgname = serializers.CharField()
    gdcglastid = serializers.IntegerField()
    level = serializers.IntegerField()
    sort = serializers.IntegerField()
    url = serializers.CharField()
    url_big = serializers.CharField()
    url_poster = serializers.CharField()

class GoodsByCateGoryForAppSerializer(serializers.Serializer):

    gdid = serializers.IntegerField()
    gd_name = serializers.CharField()
    gd_banners = serializers.SerializerMethodField()
    gd_show_price = serializers.DecimalField(max_digits=18,decimal_places=2)
    gd_mark_price = serializers.DecimalField(max_digits=18, decimal_places=2)

    def get_gd_banners(self,obj):
        return json.loads(obj.gd_banners)[0][1]

class ShopPageForAppSerializer(serializers.Serializer):

    html_data = serializers.SerializerMethodField()

    def get_html_data(self,obj):
        return json.loads(obj.html_data)

class GoodsLinkSkuSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    gdid = serializers.IntegerField()
    userid = serializers.IntegerField()
    skus = serializers.SerializerMethodField()
    image = serializers.CharField()
    price = serializers.DecimalField(max_digits=18,decimal_places=2)
    stock = serializers.IntegerField()
    item_no = serializers.CharField()
    weight = serializers.IntegerField()
    cost_price = serializers.DecimalField(max_digits=18,decimal_places=2)
    number = serializers.IntegerField()
    sort = serializers.IntegerField()

    def get_skus(self,obj):
        return obj.skus


class GoodsDetailForAppSerializer(serializers.Serializer):

    gdid = serializers.IntegerField()
    gd_name = serializers.CharField()
    gd_banners = serializers.SerializerMethodField()
    gd_show_price = serializers.DecimalField(max_digits=18,decimal_places=2)
    gd_mark_price = serializers.DecimalField(max_digits=18, decimal_places=2)
    gd_unit = serializers.CharField()
    gd_stock_tot = serializers.IntegerField()
    gd_stock_show = serializers.CharField()
    gd_specs_name_default_flag = serializers.CharField()

    gd_sku_link = serializers.SerializerMethodField()
    attribute = serializers.SerializerMethodField()

    shoppage = serializers.SerializerMethodField()

    def get_gd_banners(self,obj):
        return json.loads(obj.gd_banners)

    def get_shoppage(self,obj):

        return ShopPageForAppSerializer(obj.shoppage,many=False).data

    def get_attribute(self,obj):
        if obj.gd_specs_name_default_flag == '0':
            return [
                {
                    "sortNum":1,
                    "value_list":[{"spec_id":0,"spec_value":obj.gd_specs_name_default}],
                    "group_id":0,
                    "group_name":"默认"
                }
            ]
        else:
            return json.loads(obj.attribute)

    def get_gd_sku_link(self,obj):
        if obj.gd_specs_name_default_flag == '0':
            return [
                {
                    "id":0,
                    "skus":[
                        {
                            "spec_id":0,
                            "spec_value":obj.gd_specs_name_default,
                            "group_id":0,
                            "group_name":"默认"
                        }
                    ],
                    "image":json.loads(obj.gd_banners)[0][1],
                    "price":float(obj.gd_show_price.quantize(Decimal('0.00'))),
                    "stock":obj.gd_stock_tot
                }
            ]
        else:
            return GoodsLinkSkuSerializer(obj.gd_sku_link,many=True).data
