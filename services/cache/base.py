
import json

class RedisBase(object):

    def __init__(self,**kwargs):
        self.redis = kwargs.get("redis")
        self.key = str(kwargs.get("key"))

    async def set_dict(self,value):
        await self.redis.set(self.key,json.dumps(value))

    async def get_dict(self):
        res = await self.redis.get(self.key)
        return json.loads(res) if res else res

    async def delete(self,key):
        await self.redis.delete(key)
