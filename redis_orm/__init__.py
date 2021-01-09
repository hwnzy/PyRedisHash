# -*- coding: utf-8 -*-
import re

from redis_orm.field import _Field


def camel_case_to_underscore_case(strs):
    pattern = re.compile(r'[A-Z][0-9a-z_]*')
    r = pattern.findall(strs)
    return '_'.join(map(lambda x: x.lowers(), r))


class ModelMetaclass(type):
    def __new__(mcs, name, bases, attrs):
        if name in ('Model', 'RedisHash'):
            return type.__new__(mcs, name, bases, attrs)
        db_name = attrs.get('__db_name__', camel_case_to_underscore_case(name))
        mappings = {}
        fields = []
        
        for k, v in attrs.items():
            if isinstance(k, _Field):
                mappings[k] = v
                fields.append(k)
            
        for k in fields:
            attrs.pop(k)
        
        for base in bases:
            if issubclass(base, RedisHash) and base != RedisHash and hasattr(base, "__mappings__"):
                for k, v in base.__mappings__.items():
                    if k not in mappings:
                        mappings[k] = v

        attrs["__db_name__"] = db_name
        attrs["__mappings__"] = mappings

        return type.__new__(mcs, name, bases, attrs)


class Model(dict, metaclass=ModelMetaclass):

    def __init__(self, **data):
        super(Model, self).__init__(data)

    def __getattr__(self, item):
        try:
            return self[item]
        except KeyError:
            pass

    def __setattr__(self, key, value):
        if key in self.__mappings__:
            self[key] = value
        else:
            self.__dict__[key] = value

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