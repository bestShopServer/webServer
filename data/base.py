

from data.city import city
import json

class dataBase(object):

    def __init__(self,**kwargs):

        self.key = "static_data"
        self.redis = kwargs.get("redis")

    async def set_hash(self, dictKey, value):
        await self.redis.hset(self.key, dictKey, json.dumps(value))

    async def get_hash(self, dictKey):
        res = await self.redis.hget(self.key, dictKey)
        return json.loads(res) if res else res

class datacity(dataBase):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        self.city_key = "city"

    async def set(self):
        await self.set_hash(self.city_key,city)

    async def get(self):
        return await self.get_hash(self.city_key)


class dataAllInit(object):

    async def run(self,redis):
        await datacity(redis=redis).set()


if __name__ == '__main__':
    import os,sys
    import asyncio
    import aioredis
    PROJECT_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.path.pardir)

    if PROJECT_PATH not in sys.path:
        sys.path.insert(0, PROJECT_PATH)

    from config import config_insert

    async def go():
        redis = await aioredis.create_redis(
            (config_insert['redis']['host'], config_insert['redis']['port']), password=config_insert['redis']['password'], loop=loop)
        await dataAllInit().run(redis=redis)
        print(await datacity(redis=redis).get())
        redis.close()
        await redis.wait_closed()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(go())