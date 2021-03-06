
from utils.time_st import UtilTime

class idGenerator(object):

    def __init__(self, *args,**kwargs):
        self.redis = kwargs.get("redis")
        self.key = None

    async def userid(self,rolecode):
        self.key = str(rolecode)
        return "%s%08d" % (self.key, await self.redis.incr(self.key))

    async def ordercode(self):
        t = UtilTime().arrow_to_string(format_v="YYYYMMDDHHmmss")
        self.key = t
        res = "HG%s%03d"%(self.key,await self.redis.incr(self.key))
        await self.redis.expire(self.key,10)
        return res

    async def refund(self):
        t = UtilTime().arrow_to_string(format_v="YYYYMMDDHHmmss")
        self.key = t
        res = "RE%s%03d"%(self.key,await self.redis.incr(self.key))
        await self.redis.expire(self.key,10)
        return res

    async def goodscategory(self,level):
        self.key= "goodscategoryById"
        print(level)
        return "%s%d%06d" % ("GC",level, await self.redis.incr(self.key))

    async def goods(self):
        self.key="goodsById"
        return "%s%07d"%("G",await self.redis.incr(self.key))