
import json
from rest_framework import serializers

from utils.time_st import UtilTime

class OrderDetailSerializerForOrder(serializers.Serializer):

    name = serializers.CharField()
    phone = serializers.CharField()
    source = serializers.CharField()
    pay_type = serializers.CharField()

    user = serializers.SerializerMethodField()


    def get_user(self,obj):
        return UserSerializerForOrder(obj.user, many=False).data

class OrderListSerializerForOrder(serializers.Serializer):

    gd_img = serializers.CharField()
    gd_name = serializers.CharField()
    gd_price = serializers.CharField()
    gd_number = serializers.CharField()
    gd_unit = serializers.CharField()
    gd_sku_name = serializers.CharField()
    gd_sku_id = serializers.IntegerField()

class UserSerializerForOrder(serializers.Serializer):

    name = serializers.CharField()
    userid = serializers.IntegerField()

class OrderSerializerForOrder(serializers.Serializer):

    orderid = serializers.CharField()
    createtime = serializers.SerializerMethodField()
    status = serializers.CharField()
    orderdetail = serializers.SerializerMethodField()
    orderlist = serializers.SerializerMethodField()
    pay_amount = serializers.DecimalField(max_digits=18,decimal_places=2)

    def get_createtime(self,obj):

        return UtilTime().timestamp_to_string(obj.createtime)


    def get_orderdetail(self,obj):

        return OrderDetailSerializerForOrder(obj.orderdetail,many=False).data

    def get_orderlist(self,obj):

        return OrderListSerializerForOrder(obj.orderlist,many=True).data


class UserSerializerForOrderDetail(serializers.Serializer):

    name = serializers.CharField()
    userid = serializers.IntegerField()

class OrderDetailSerializerForOrderDetail(serializers.Serializer):

    name = serializers.CharField()
    phone = serializers.CharField()
    pay_type = serializers.CharField()

    memo = serializers.CharField()

    user = serializers.SerializerMethodField()

    province_code = serializers.CharField()
    province_name = serializers.CharField()

    city_code = serializers.CharField()
    city_name = serializers.CharField()

    county_code = serializers.CharField()
    county_name = serializers.CharField()

    detail = serializers.CharField()


    def get_user(self,obj):
        return UserSerializerForOrderDetail(obj.user, many=False).data

class OrderListSerializerForOrderDetail(serializers.Serializer):

    gd_img = serializers.CharField()
    gd_name = serializers.CharField()
    gd_price = serializers.CharField()
    gd_number = serializers.CharField()
    gd_unit = serializers.CharField()
    gd_sku_name = serializers.CharField()
    gd_sku_id = serializers.IntegerField()
    gd_item_no = serializers.CharField()
    fare_no = serializers.CharField()
    fare_status = serializers.CharField()


class OrderSerializerForOrderDetail(serializers.Serializer):

    status = serializers.CharField()
    status_list = serializers.SerializerMethodField()
    pay_amount = serializers.DecimalField(max_digits=18,decimal_places=2)
    orderdetail = serializers.SerializerMethodField()
    orderlist = serializers.SerializerMethodField()

    def get_status_list(self,obj):
        return json.loads(obj.status_list)

    def get_orderdetail(self,obj):

        return OrderDetailSerializerForOrderDetail(obj.orderdetail,many=False).data

    def get_orderlist(self,obj):

        return OrderListSerializerForOrderDetail(obj.orderlist,many=True).data