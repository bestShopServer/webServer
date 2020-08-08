
import json
from rest_framework import serializers
from utils.time_st import UtilTime

class ShopPageDetailForAppSerializer(serializers.Serializer):
    title = serializers.CharField()
    html_data = serializers.SerializerMethodField()

    def get_html_data(self,obj):
        return json.loads(obj.html_data)
