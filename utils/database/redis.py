
import aioredis
from tornado.options import options

async def _init_with_loop(loop):
    """
    redis 连接池
    :param loop: 循环
    :return: redis pool
    """
    __pool = await aioredis.create_redis_pool(
        'redis://{}:{}'.format(options.redis_host,options.redis_port),
        minsize=options.redis_minsize,
        maxsize=options.redis_maxsize,
        password=options.redis_password,
        encoding=options.redis_encoding,
        loop=loop)
    return __pool


class RedisPool:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            _loop = kwargs.get("loop", None)
            assert _loop, "use get_event_loop()"
            cls._redis = _loop.run_until_complete(_init_with_loop(_loop))
            cls._instance = super(RedisPool, cls).__new__(cls)
        return cls._instance

    def get_conn(self) -> aioredis.Redis:
        return self._redis
