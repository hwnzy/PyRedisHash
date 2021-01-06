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