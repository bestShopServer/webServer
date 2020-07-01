

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