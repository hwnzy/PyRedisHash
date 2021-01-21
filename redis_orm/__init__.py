# -*- coding: utf-8 -*-
import re
import time
import redis

from redis_orm.field import _Field

REDIS = {}


def camel_case_to_underscore_case(strs):
    pattern = re.compile(r'[A-Z][0-9a-z_]*')
    r = pattern.findall(strs)
    return '_'.join(map(lambda x: x.lowers(), r))


def db_init():
    REDIS['system_name'] = redis.StrictRedis(host='localhost', port=6379, db=0)


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

    _last_storage = 0

    _STORAGE_INTERVAL = 300

    _KEY = '{}:{}'

    def __init__(self, **kwargs):
        self._db = REDIS[self.__db_name__]
        self._key = self._KEY.format(self._db, '123456')

        data = {}

        if self.__mappings__:
            redis_data = self._db.hgetall(self._key)
            for k, v in self.__mappings__.items():
                if k in redis_data:
                    data[k] = v.to_py(redis_data[k])
                else:
                    data[k] = v.default

        data.update(kwargs)

        super(RedisHash, self).__init__(**data)

    def store(self, force=False):
        try:
            now = int(time.time())
            if self._last_storage + self._STORAGE_INTERVAL < now or force:
                data = {}
                for k, v in self.__mappings__.items():
                    data[k] = v.to_redis(self.get(k, v.default))
                storage_time = self.get_storage_time()

                if data:
                    self._db.hmset(self._key, data)
                    if storage_time:
                        self._db.expire(self._key, storage_time)
                    self._last_storage = now
        except Exception as e:
            pass

    @classmethod
    def hgetall(cls, user_id):
        ret = REDIS[cls.__db_name__].hgetall(cls._KEY.format(cls.__db_name__, user_id))
        return ret
    
    @classmethod
    def hset(cls, user_id, key, value):
        ret = REDIS[cls.__db_name__].hset(cls._KEY.format(cls.__db_name__, user_id), key, value)
        return ret

    @classmethod
    def hmset(cls, user_id, k_values):
        ret = REDIS[cls.__db_name__].hmset(cls._KEY.format(cls.__db_name__, user_id), k_values)
        return ret

    @classmethod
    def hget(cls, user_id, key):
        ret = REDIS[cls.__db_name__].hget(cls._KEY.format(cls.__db_name__, user_id), key)
        return ret

    @classmethod
    def hmget(cls, user_id, *keys):
        ret = REDIS[cls.__db_name__].hmget(cls._KEY.format(cls.__db_name__, user_id), *keys)
        return ret

    @classmethod
    def delete(cls, user_id):
        ret = REDIS[cls.__db_name__].delete(cls._KEY.format(cls.__db_name__, user_id))
        return ret

    @classmethod
    def expire(cls, user_id, ts):
        ret = REDIS[cls.__db_name__].expire(cls._KEY.format(cls.__db_name__, user_id), ts)
        return ret
