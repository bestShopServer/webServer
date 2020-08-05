
import json
from decimal import Decimal
from rest_framework import serializers
from utils.time_st import UtilTime


class UserForAppSerializer(serializers.Serializer):

    pic = serializers.CharField()
    name = serializers.CharField()
    token = serializers.CharField()
