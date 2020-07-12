

import json
from rest_framework import serializers

from utils.time_st import UtilTime


class SkuSpecValueSerializer(serializers.Serializer):

    spec_id = serializers.IntegerField()
    group_id = serializers.IntegerField()
    spec_value = serializers.CharField()

class SkuGroupSerializer(serializers.Serializer):

    group_id = serializers.IntegerField()
    group_name = serializers.CharField()

    spec_values = serializers.SerializerMethodField()

    def get_spec_values(self,obj):
        return SkuSpecValueSerializer(obj.spec_values,many=True).data

class GoodsCateGoryStyleSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    type = serializers.IntegerField()
    typecode = serializers.CharField()

class GoodsCateGorySerializer(serializers.Serializer):

    gdcgid = serializers.IntegerField()
    gdcgname = serializers.CharField()
    gdcglastid = serializers.IntegerField()
    level = serializers.IntegerField()
    sort = serializers.IntegerField()
    status = serializers.CharField()
    url = serializers.CharField()
    url_big = serializers.CharField()
    url_poster = serializers.CharField()

class GoodsSerializer(serializers.Serializer):

    gdid = serializers.IntegerField()
    gd_name = serializers.CharField()
    gd_banners = serializers.SerializerMethodField()
    gd_show_price = serializers.DecimalField(max_digits=18,decimal_places=2)
    gd_mark_price = serializers.DecimalField(max_digits=18, decimal_places=2)
    gd_stock_tot = serializers.IntegerField()
    gd_sell_tot_number = serializers.SerializerMethodField()
    gd_status = serializers.SerializerMethodField()
    createtime = serializers.SerializerMethodField()

    def get_gd_status(self,obj):
        return "销售中" if obj.gd_status == '0' else '下架'

    def get_gd_banners(self,obj):
        return json.loads(obj.gd_banners)[0][1]

    def get_gd_sell_tot_number(self,obj):
        return obj.gd_sell_actual_number + obj.gd_sell_number

    def get_createtime(self,obj):
        return UtilTime().timestamp_to_string(obj.createtime)

class GoodsLinkCitySerializer(serializers.Serializer):

    id = serializers.IntegerField()
    userid = serializers.IntegerField()
    gdid = serializers.IntegerField()
    citycode = serializers.CharField()
    cityname = serializers.CharField()


class GoodsLinkCateGorySerializer(serializers.Serializer):

    id = serializers.IntegerField()
    userid = serializers.IntegerField()
    gdid = serializers.IntegerField()
    gdcgid = serializers.IntegerField()
    gdcgname = serializers.SerializerMethodField()


    def get_gdcgname(self,obj):

        return obj.goodscategory.gdcgname if hasattr(obj,'goodscategory') else obj.gdcgname

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

class GoodsDetailSerializer(serializers.Serializer):

    gdid = serializers.IntegerField()
    userid = serializers.IntegerField()

    gd_name = serializers.CharField()
    gd_banners = serializers.SerializerMethodField()
    gd_status = serializers.CharField()
    gd_sort = serializers.IntegerField()

    """
    价格库存
    """
    gd_show_price = serializers.DecimalField(max_digits=18,decimal_places=2)
    gd_mark_price = serializers.DecimalField(max_digits=18,decimal_places=2)
    gd_unit = serializers.CharField()
    gd_cost_price = serializers.DecimalField(max_digits=18,decimal_places=2)

    gd_stock_tot = serializers.IntegerField()
    gd_stock_show = serializers.CharField()
    gd_specs_name_default_flag = serializers.CharField()
    gd_specs_name_default = serializers.CharField()

    gd_item_no = serializers.CharField()
    gd_weight = serializers.IntegerField()

    gd_sku_link = serializers.SerializerMethodField()

    gd_sell_actual_number = serializers.IntegerField()

    """
    购买设置
    """
    gd_sell_number = serializers.IntegerField()
    gd_fare_mould_id = serializers.IntegerField()
    gd_fare_mould_name = serializers.SerializerMethodField()
    gd_limit_number_by_goods = serializers.IntegerField()
    gd_limit_number_by_order = serializers.IntegerField()

    gd_include_fare1 = serializers.IntegerField()
    gd_include_fare2 = serializers.DecimalField(max_digits=18,decimal_places=2)
    gd_allow_area_flag = serializers.CharField()

    """
    分享图片
    """
    gd_share_title = serializers.CharField()
    gd_share_image = serializers.CharField()
    createtime = serializers.SerializerMethodField()

    gd_link_type = serializers.SerializerMethodField()
    gd_allow_area = serializers.SerializerMethodField()

    attribute = serializers.CharField()

    def get_gd_fare_mould_name(self,obj):
        return obj.gd_fare_rule.fare_rule_name if obj.gd_fare_rule else ""

    def get_gd_banners(self,obj):
        return json.loads(obj.gd_banners)

    def get_createtime(self,obj):
        return UtilTime().timestamp_to_string(obj.createtime)

    def get_gd_sku_link(self,obj):
        return GoodsLinkSkuSerializer(obj.gd_sku_link,many=True).data

    def get_gd_link_type(self,obj):
        return GoodsLinkCateGorySerializer(obj.gd_link_type,many=True).data

    def get_gd_allow_area(self,obj):
        return GoodsLinkCitySerializer(obj.gd_allow_area,many=True).data
