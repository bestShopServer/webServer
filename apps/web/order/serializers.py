
import json
from rest_framework import serializers

from utils.time_st import UtilTime

class OrderDetailSerializerForOrder(serializers.Serializer):

    pay_type = serializers.CharField()
    name = serializers.CharField()
    phone = serializers.CharField()

class OrderListSerializerForOrder(serializers.Serializer):

    gd_img = serializers.CharField()
    gd_name = serializers.CharField()
    gd_price = serializers.CharField()
    gd_number = serializers.CharField()
    gd_unit = serializers.CharField()

class UserSerializerForOrder(serializers.Serializer):

    name = serializers.CharField()

class OrderSerializerForOrder(serializers.Serializer):

    orderid = serializers.CharField()
    createtime = serializers.SerializerMethodField()
    status = serializers.CharField()

    def get_createtime(self,obj):

        return UtilTime().timestamp_to_string(obj.createtime)