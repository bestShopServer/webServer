
import json
from rest_framework import serializers
from utils.time_st import UtilTime

class ShopPageForAppSerializer(serializers.Serializer):

    html_data = serializers.SerializerMethodField()

    def get_html_data(self,obj):
        return json.loads(obj.html_data)

class ShopConfigForAppSerializer(serializers.Serializer):

    navigation_data = serializers.SerializerMethodField()

    def get_navigation_data(self,obj):
        return json.loads(obj.navigation_data)

class GoodsCateGoryStyleForAppSerializer(serializers.Serializer):

    typecode = serializers.CharField()
    type = serializers.CharField()

class GoodsCateGoryForAppSerializer(serializers.Serializer):

    gdcgid = serializers.IntegerField()
    gdcgname = serializers.CharField()
    gdcglastid = serializers.IntegerField()
    level = serializers.IntegerField()
    sort = serializers.IntegerField()
    status = serializers.CharField()
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