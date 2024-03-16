import redis
from app.settings import REDIS_HOST, REDIS_PORT
from typing import Generator

class RedisDB:
    __redis_connect = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

    @classmethod
    def set_pair(cls, key: str, value: str, ex: int | None = None) -> None:
        cls.__redis_connect.set(key, value, ex)

    @classmethod
    def get_pair(cls, key: str) -> str | None:
        value = cls.__redis_connect.get(key)
        if value:
            value = value.decode('utf-8')
            return value
        return None

    @classmethod
    def drop_pair(cls, key: str) -> int | None:
        n = cls.__redis_connect.delete(key)
        return n
    
    def __getitem__(self, key: str) -> int | None:
        return self.get_pair(key)


    def __setitem__(self, key: str|slice, value: str):
        if isinstance(key, slice):
            return self.set_pair(key.start, value, key.stop)
        return self.set_pair(key, value)
    
    def __contains__(self, item):
        return self.get_pair(item) is not None
    
    def __delitem__(self, item):
        return self.drop_pair(item)


async def get_db():
    db = RedisDB()
    yield db