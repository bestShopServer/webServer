

from rest_framework import serializers

class AttachMentGroupSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    name = serializers.CharField()
    type = serializers.CharField()

class AttachMentSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    name = serializers.CharField()
    type = serializers.CharField()
    url = serializers.CharField()
    grouid = serializers.IntegerField()


class MenuSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    parent_id = serializers.IntegerField()
    title = serializers.CharField()
    type = serializers.CharField()
    pic = serializers.CharField()
    sort = serializers.IntegerField()
    component = serializers.CharField()
    component_name = serializers.CharField()
    path = serializers.CharField()
    keep = serializers.CharField()
    status = serializers.CharField()
    premission = serializers.CharField()
