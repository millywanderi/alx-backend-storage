#!/usr/bin/env python3
"""
A module that creates a cache class to store redis instances
"""
import redis
import uuid
from typing import Union, Callable, Optional, Any
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    A system that counts how many times methods of the Cache class are called
    """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """wrap"""
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """Function that add its input parametes one list in redis"""
    key = method.__qualname__
    inputs = key + ":inputs"
    outputs = key + ":outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """wrap"""
        self._redis.rpush(inputs, str(args))
        data = method(self, *args, **kwargs)
        self._redis.rpush(outputs, str(data))
        return data
    return wraper


def replay(method: Callable) -> None:
    """Replays the history of a function"""
    name = method.__qualname__
    cache = redis.Redis()
    calls = cache.get(name).decode("utf-8")
    print("{} was called {} times:".format(name, calls))
    inputs = cache.lrange(name + ":inputs", 0, -1)
    outputs = cache.lrange(name + ":outputs", 0, -1)
    for i, o in zip(inputs, outputs):
        print("{}(*{}) -> {}".format(name, i.decode('utf-8'),
                                     o.decode('utf-8')))


class Cache:
    def __init__(self) -> None:
        """Initializes the class Cache"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Stores data in redis caches"""
        key = str(uuid.uuid4())
        self.__redis.set(key, data)

        return key

    def get(self, key: str, fn: Optiopnal[Callable] = None)\
            -> Union[str, bytes, int, float, None]:
        """Get data from the reddis Cache"""
        data = self._redis.get(key)
        if data is not None and fn is not none and callable(fn):
            return data

    def get_str(self, key: str) -> str:
        """Get data as a string from redis cache"""
        data = self.get(key, lambda x: x.decode('utf-8'))
        return data

    def get_int(self, key: str) -> int:
        """Get data as integer from redis cache"""
        return self.get(key, int)
