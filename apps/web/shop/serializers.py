

import json
from rest_framework import serializers
from utils.time_st import UtilTime


class ShopPageSerializer(serializers.Serializer):
    id =  serializers.IntegerField()
    userid =  serializers.IntegerField()
    title = serializers.CharField()
    time_publish_flag = serializers.CharField()
    time_publish = serializers.SerializerMethodField()
    html_data = serializers.SerializerMethodField()

    def get_html_data(self,obj):
        return json.loads(obj.html_data)

    def get_time_publish(self,obj):
        return UtilTime().timestamp_to_string(obj.time_publish) if obj.time_publish else ""


