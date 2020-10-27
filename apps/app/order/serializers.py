


import json
from rest_framework import serializers
from utils.time_st import UtilTime

class AddressForAppSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    name = serializers.CharField()
    mobile = serializers.CharField()

    province_code = serializers.CharField()
    province_name = serializers.CharField()

    city_code = serializers.CharField()
    city_name = serializers.CharField()

    county_code = serializers.CharField()
    county_name = serializers.CharField()

    address_detail = serializers.CharField()
    address_default = serializers.CharField()

class ShopCartForAppSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    gdid = serializers.IntegerField()

    gd_img = serializers.CharField()
    gd_name = serializers.CharField()
    gd_price = serializers.DecimalField(max_digits=18,decimal_places=2)
    gd_number = serializers.IntegerField()
    gd_item_no = serializers.CharField()
    gd_weight = serializers.IntegerField()
    gd_sku_id = serializers.IntegerField()
    gd_sku_name = serializers.CharField()
    gd_unit = serializers.CharField()

class OrderListForAppSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    gdid = serializers.IntegerField()

    gd_img = serializers.CharField()
    gd_name = serializers.CharField()
    gd_price = serializers.DecimalField(max_digits=18,decimal_places=2)
    gd_number = serializers.IntegerField()
    gd_sku_id = serializers.IntegerField()
    gd_sku_name = serializers.CharField()
    gd_unit = serializers.CharField()

    fare_amount = serializers.DecimalField(max_digits=18,decimal_places=2)

class OrderDetailForAppSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    memo = serializers.CharField()
    pay_type = serializers.CharField()

    name = serializers.CharField()
    phone = serializers.CharField()

    province_code = serializers.CharField()
    province_name = serializers.CharField()

    city_code = serializers.CharField()
    city_name = serializers.CharField()

    county_code = serializers.CharField()
    county_name = serializers.CharField()

    detail = serializers.CharField()

class OrderForAppSerializer(serializers.Serializer):

    orderid = serializers.CharField()
    status = serializers.CharField()
    fare_amount = serializers.DecimalField(max_digits=18,decimal_places=2)
    pay_amount = serializers.DecimalField(max_digits=18,decimal_places=2)
    orderlist = serializers.SerializerMethodField()

    def get_orderlist(self,obj):
        return OrderListForAppSerializer(obj.orderlist,many=True).data

class OrderRefundSerializerForAppSerializer(serializers.Serializer):

    refund_id = serializers.CharField()
    status = serializers.CharField()

class orderOrderDetailForAppSerializer(serializers.Serializer):


    orderid = serializers.CharField()
    status = serializers.CharField()
    status_list = serializers.SerializerMethodField()
    fare_amount = serializers.DecimalField(max_digits=18,decimal_places=2)
    pay_amount = serializers.DecimalField(max_digits=18,decimal_places=2)
    orderlist = serializers.SerializerMethodField()
    orderdetail = serializers.SerializerMethodField()
    orderrefund = serializers.SerializerMethodField()

    def get_orderlist(self,obj):
        return OrderListForAppSerializer(obj.orderlist,many=True).data

    def get_orderdetail(self,obj):
        return OrderDetailForAppSerializer(obj.orderdetail,many=False).data

    def get_status_list(self,obj):
        return json.loads(obj.status_list)

    def get_orderrefund(self,obj):
        return OrderRefundSerializerForAppSerializer(obj.orderrefund,many=False).data
