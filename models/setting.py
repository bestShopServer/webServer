
from peewee import *
from models.base import BaseModel


class FareRule(BaseModel):
    """
    运费规则
    """
    fare_rule_id = BigAutoField(primary_key=True,verbose_name="规则ID")
    userid = BigIntegerField(verbose_name="用户代码", null=True)
    fare_rule_name = CharField(max_length=60,verbose_name="规则名称",default="")
    fare_rule_fee_type = CharField(max_length=1,verbose_name="计费方式 0-按重计费,1-按件计费",default="1")
    fare_rule_default = CharField(max_length=1,verbose_name="是否默认,0-是,1-否",default='1')
    fare_rule_first_weight = IntegerField(verbose_name="首重(克)",default=0)
    fare_rule_first_fee = DecimalField(max_digits=18,decimal_places=6,default=0.000,verbose_name="首费(元)")
    fare_rule_join_weight = IntegerField(verbose_name="续重(克)",default=0)
    fare_rule_join_fee = DecimalField(max_digits=18,decimal_places=6,default=0.000,verbose_name="续费(元)")

    class Meta:
        db_table = 'farerule'

class FareLinkCity(BaseModel):
    """
    运费规则城市关联表
    """

    id = BigAutoField(primary_key=True,verbose_name="关联ID")
    userid = BigIntegerField(verbose_name="用户代码", null=True)
    fare_rule_id = BigIntegerField(verbose_name="运费规则ID")
    province = CharField(max_length=30,verbose_name="省/直辖市代码")
    province_name = CharField(max_length=60,verbose_name="省名称")
    city = CharField(max_length=30,verbose_name="市代码")
    city_name = CharField(max_length=60,verbose_name="市名称")
    country = CharField(max_length=30,verbose_name="县/区")
    country_name = CharField(max_length=60,verbose_name="县名称")

    class Meta:
        db_table = 'farelinkcity'