# -*- coding: utf-8 -*-
import json
import copy


class _Field(object):
    def __init__(self, name, py_type, default):
        self.name = name
        self._py_type = py_type
        self.default = default


class IntField(_Field):
    def __init__(self, name=None, py_type=int, default=0):
        super(IntField, self).__init__(name, py_type, default)
    
    def to_py(self, value):
        try:
            return int(float(value))
        except ValueError:
            return self.default


class FloatField(_Field):
    def __init__(self, name=None, py_type=float, default=0.0):
        super(FloatField, self).__init__(name, py_type, default)

    def to_py(self, value):
        try:
            return float(value)
        except ValueError:
            return self.default


class StrField(_Field):
    def __init__(self, name=None, py_type=str, default=''):
        super(StrField, self).__init__(name, py_type, default)

    def to_py(self, value):
        try:
            return str(value)
        except ValueError:
            return self.default


class DictField(_Field):
    def __init__(self, name=None, py_type=dict, default=None):
        if default is None:
            default = {}
        super(DictField, self).__init__(name, py_type, default)

    def to_py(self, value):
        try:
            return json.loads(value)
        except ValueError:
            return self.default


class ListField(_Field):
    def __init__(self, name=None, py_type=list, default=None):
        if default is None:
            default = []
        super(ListField, self).__init__(name, py_type, default)

    def to_py(self, value):
        try:
            return json.loads(value)
        except ValueError:
            return self.default
