

import json
from rest_framework import serializers
from utils.time_st import UtilTime

class ShopConfigSerializer(serializers.Serializer):
    id =  serializers.IntegerField()
    userid =  serializers.IntegerField()
    navigation_data = serializers.SerializerMethodField()

    def get_navigation_data(self,obj):
        return json.loads(obj.navigation_data)

class ShopPageSerializer(serializers.Serializer):
    id =  serializers.IntegerField()
    userid =  serializers.IntegerField()
    title = serializers.CharField()
    createtime = serializers.SerializerMethodField()
    type = serializers.CharField()

    def get_createtime(self,obj):
        return UtilTime().timestamp_to_string(obj.createtime)

class ShopPageDetailSerializer(serializers.Serializer):
    id =  serializers.IntegerField()
    userid =  serializers.IntegerField()
    title = serializers.CharField()
    time_publish_flag = serializers.CharField()
    type = serializers.CharField()
    time_publish = serializers.IntegerField()
    html_data = serializers.SerializerMethodField()

    def get_html_data(self,obj):
        return json.loads(obj.html_data)

