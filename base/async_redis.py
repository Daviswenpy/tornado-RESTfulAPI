import aioredis
from base.settings import REDIS


async def _init_with_loop(loop):
    """
    redis 连接池
    :param loop: 事件循环
    :return: redis pool
    """
    __pool = await aioredis.create_redis_pool(REDIS.get('default').get('LOCATION'), minsize=1, maxsize=10000, encoding='utf8', loop=loop)
    return __pool


class RedisPool(object):
    '''
    使用单例模式
    '''
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            _loop = kwargs.get("loop", None)
            assert _loop, "use get_event_loop()"
            cls._redis = _loop.run_until_complete(_init_with_loop(_loop))
            cls._instance = super(RedisPool, cls).__new__(cls)
        return cls._instance

    def get_conn(self) -> aioredis.Redis:
        return self._redis