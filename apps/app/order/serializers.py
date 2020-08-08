


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