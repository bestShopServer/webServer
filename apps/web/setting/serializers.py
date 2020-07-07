


from rest_framework import serializers


class FareLinkCitySerializer(serializers.Serializer):
    id =  serializers.IntegerField()
    userid =  serializers.IntegerField()
    fare_rule_id =  serializers.IntegerField()
    province = serializers.CharField()
    province_name = serializers.CharField()
    city = serializers.CharField()
    city_name = serializers.CharField()
    country = serializers.CharField()
    country_name = serializers.CharField()

class FareRuleSerializer(serializers.Serializer):

    fare_rule_id = serializers.IntegerField()
    userid = serializers.IntegerField()
    fare_rule_name = serializers.CharField()
    fare_rule_fee_type = serializers.CharField()
    fare_rule_default = serializers.CharField()
    fare_rule_first_weight = serializers.IntegerField()
    fare_rule_first_fee = serializers.DecimalField(max_digits=18,decimal_places=2)
    fare_rule_join_weight = serializers.IntegerField()
    fare_rule_join_fee = serializers.DecimalField(max_digits=18,decimal_places=2)
    fare_rule_link_citys = serializers.SerializerMethodField()


    def get_fare_rule_link_citys(self,obj):

        return FareLinkCitySerializer(obj.fare_rule_link_citys,many=True).data


