
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