
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

    async def delete(self):
        await self.redis.delete(self.key)

    async def set_hash(self, dictKey, value):
        await self.redis.hset(self.key, dictKey, json.dumps(value))

    async def get_hash(self, dictKey):
        res = await self.redis.hget(self.key, dictKey)
        return json.loads(res) if res else res

    async def del_hash(self, dictKey):
        await self.redis.hdel(self.key, dictKey)

    async def delall_hash(self):
        await self.redis.delete(self.key)

    async def getall_hash(self):

        res = await self.redis.hgetall(self.key)
        res_ex = {}
        if res:
            for key in res:
                res_ex[key.decode()] = json.loads(res[key])
        return res_ex if res else None
