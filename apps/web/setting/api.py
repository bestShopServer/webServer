
from utils.decorator.connector import Core_connector

from apps.base import BaseHandler
from apps.web.setting.rule import FareRuleRules

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