
from utils.decorator.connector import Core_connector

from utils.exceptions import PubErrorCustom

from apps.base import BaseHandler
from apps.web.setting.rule import FareRuleRules
from models.setting import FareRule

class farerule(BaseHandler):
    """
    运费规则配置
    """

    @Core_connector(**FareRuleRules.post())
    async def post(self, *args, **kwargs):
        pass

    @Core_connector(**FareRuleRules.put())
    async def put(self, *args, **kwargs):
        pass

    @Core_connector(**FareRuleRules.delete())
    async def delete(self, *args, **kwargs):
        pass

    @Core_connector(**FareRuleRules.get())
    async def get(self, *args, **kwargs):
        pass

class farerule_default_setting(BaseHandler):
    """
    运费默认规则设置
    """
    @Core_connector()
    async def put(self, pk=None):

        fare_rule_default = self.data.get("fare_rule_default",None)
        if not fare_rule_default:
            raise PubErrorCustom("请选择是否默认!")

        for item in await self.db.execute(FareRule.select().for_update().where(FareRule.userid==self.user['userid'])):
            if pk == item.fare_rule_id:
                item.fare_rule_default = fare_rule_default
            else:
                item.fare_rule_default = '1'
            await self.db.update(item)