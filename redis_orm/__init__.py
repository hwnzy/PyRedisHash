# -*- coding: utf-8 -*-

class ModelMetaclass(type):
    def __new__(cls, *args, **kwargs):
        pass


class Model(dict, metaclass=ModelMetaclass):
    def __init__(self):
        pass

    def __getattr__(self, item):
        pass

    def __setattr__(self, key, value):
        pass

    def save(self):
        pass

class RedisHash(Model):
    def __init__(self):
        super(RedisHash, self).__init__()

    def store(self, force=False):
        pass

    @classmethod
    def hgetall(cls, k):
        pass
    
    @classmethod
    def hset(cls, k, key, value):
        pass

    @classmethod
    def hmset(cls, k, k_values):
        pass

    @classmethod
    def hget(cls, k):
        pass

    @classmethod
    def hmget(cls, *keys):
        pass

    @classmethod
    def delete(cls, k):
        pass

    @classmethod
    def expire(cls, k):
        pass