# -*- coding:utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
import inspect
import sys
import types
import urwid

from . import constants as C
from . import settings as S
from .utils import pyv, _unicode
from .terminal_size import get_terminal_size
from .lib import search_up_tree as sut
# from kitchen.text import display

if pyv == 2:
    range = xrange


def ustr(s):
    '''convert string into unicode'''
    res = u''

    if not isinstance(s, (_unicode, str)):
        s = str(s)

    if isinstance(s, _unicode):
        res += s
    elif isinstance(s, str):
        # in python 2/3, it's utf8
        # so decode to unicode
        res += s.decode(S.encoding)

    return res

def long_string_wrapper(ls, how):
    if how == C._LS_WRAP_BY_80_COLUMN:
        pass
    pass

def tail_symbol(position):
    """calculate the tail of block
    newline character does not include here because
    when your calculate the length of whole line you only need to be
    care about printable characters
    """
    if (position & C._AS_LIST_ELEMENT_ or
            position & C._AS_DICT_ELEMENT_ or
            position & C._AS_CLASS_ELEMENT_ or
            position & C._AS_TUPLE_ELEMENT_):
        tail = u','
    else:
        tail = u''
    return tail


def is_extendable(obj):
    '判断obj是否可以展开'
    return isinstance(obj, dict) or hasattr(obj, '__dict__') or isinstance(obj, (tuple, list, types.FrameType))


def object_attr_default_filter(obj, name, val):
    '过滤不需要的对象属性'

    for propLeading in S.prop_leading_filters:
        if name.startswith(propLeading):
            return True

    for prop in S.prop_filters:
        # filter is a string
        if isinstance(prop, str) or isinstance(prop, _unicode):
            if name == prop:
                return True
        # filter is a type
        # if type(prop) == types.TypeType:
        if isinstance(prop, type):
            if type(val) == prop:
                return True
        # filter is callable
        elif hasattr(prop, '__call__'):
            if prop(name, val):
                return True

    return False

def dict_key_filter(obj, name, val):
    return False

def _b(s):
    if S.write_to_buffer_when_execute:
        S.buffer_handler.write(s)
        S.buffer_handler.flush()
    return s
