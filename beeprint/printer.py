# -*- coding:utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
import sys
import traceback
import types
import inspect

from .utils import pyv
import urwid

if pyv == 2:
    # avoid throw [UnicodeEncodeError: 'ascii' codec can't encode characters]
    # exceptions, without these lines, the sys.getdefaultencoding() returns ascii
    from imp import reload

    reload(sys)
    sys.setdefaultencoding('utf-8')
else:
    unicode = str

from . import settings as S
from . import constants as C
from . import utils
from .utils import print_exc_plus
from .helper import typeval, pstr, tail_symbol, is_extendable, too_long
from .debug_kit import debug
from . import models
from .block_helper import pair_block_key



def beeprint(o, output=True):
    """print data beautifully

    >>> beeprint(1)
    1

    >>> beeprint(1.1)
    1.1

    >>> beeprint(-1)
    -1

    >>> beeprint(-1.1)
    -1.1

    >>> beeprint("plain string")
    'plain string'

    >>> beeprint(u'unicode string')
    'unicode string'

    >>> beeprint(u'utf8 string'.encode('utf-8'))
    'utf8 string'

    >>> beeprint(u'gb2312 string'.encode('gb2312'))
    'gb2312 string'

    >>> beeprint(u'\\\\')
    '\\'

    >>> beeprint(u'\\\\'.encode("utf8"))
    '\\'
    """
    res = build_single_block(o, 0)
    if output and not S.write_to_buffer_when_execute:
        try:
            print(res, end='')
        except Exception as e:
            print_exc_plus()
            if type(e) is UnicodeEncodeError:
                # UnicodeEncodeError: 'ascii' codec can't encode characters in
                # position 35-36: ordinal not in range(128)
                print(sys.getdefaultencoding())
                print('res value type:', type(res))
            else:
                print('exception type :', type(e))
    else:
        return res

def object_attr_default_filter(obj, name, val):
    '过滤不需要的对象属性'

    for propLeading in S.prop_leading_filters:
        if name.startswith(propLeading):
            return True

    for prop in S.prop_filters:
        # filter is a string
        if isinstance(prop, str) or isinstance(prop, unicode):
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


def build_single_block(obj, leadCnt=0, position=C._AS_ELEMENT_):
    '遍历对象，判断对象内成员的类型，然后调用对应的 build_*_block() 处理'

    debug(C._DL_FUNC_, leadCnt,
          ('obj:%s leadCnt:%s position:%d' \
           % (obj, leadCnt, position)))

    ret = pstr('')

    tail = tail_symbol(position)

    if S.max_depth < leadCnt:
        if S.newline or position & C._AS_ELEMENT_:
            ret = pstr(leadCnt * S.leading) + pstr("<OUT OF RANGE>\n")
        else:
            ret = pstr(" ") + pstr("<OUT OF RANGE>\n")
        if position & C._AS_LIST_ELEMENT_:
            ret = ret[:-1] + pstr(tail + "\n")
        return _b(ret)

    if isinstance(obj, dict):
        debug(C._DL_STATEMENT, leadCnt, 'is dict')
        ret += build_dict_block(obj, leadCnt, position)
    elif isinstance(obj, list):
        debug(C._DL_STATEMENT, leadCnt, 'is list')
        ret += build_list_block(obj, leadCnt, position)
    elif isinstance(obj, tuple):
        debug(C._DL_STATEMENT, leadCnt, 'is tuple')
        ret += build_tuple_block(obj, leadCnt, position)
    # hasattr(obj, '__dict__') or isinstance(obj, object):
    elif is_extendable(obj):
        debug(C._DL_STATEMENT, leadCnt, 'is extendable')
        ret += build_class_block(obj, leadCnt, position)
    else:
        debug(C._DL_STATEMENT, leadCnt, 'is simple type')
        context = models.Context(indent_char=S.leading, position=position, lead_cnt=leadCnt)
        ret += _b(leadCnt * S.leading + typeval(context, obj) + pstr(tail + '\n'))

    return ret

def build_pair_block(name, val, leadCnt=0, position=C._AS_ELEMENT_):
    debug(C._DL_FUNC_, leadCnt,
          ('key:%s, leadCnt:%s, position:%s' \
           % (name, leadCnt, position)))
    ret = pstr('')

    tail = tail_symbol(position)

    key = pair_block_key(position, name)

    ret += _b(S.leading * leadCnt + key + ':')
    if is_extendable(val) and S.max_depth > leadCnt:
        # value need to be dispalyed on new line
        # including: 
        #   class type & class instance
        #   function type
        if S.newline or (is_newline_obj(val) &
                             position & C._AS_ELEMENT_):
            ret += _b(pstr('\n'))
            leadCnt = leadCnt + 1
            position |= C._AS_ELEMENT_
            debug(C._DL_STATEMENT, leadCnt, 'make newline')
        # value will be dispalyed immediately after one space
        else:
            ret += _b(pstr(" "))
            position |= C._AS_VALUE_

        ret += build_single_block(val, leadCnt, position)
    else:
        if S.max_depth <= leadCnt:
            ret += _b(pstr(" <OUT OF RANGE>%s\n" % tail))
        else:
            context = models.Context(indent_char=S.leading, 
                                     position=position,
                                     lead_cnt=leadCnt,
                                     key=name)
            ret += _b(pstr(" ") + typeval(context, val) + pstr(tail + '\n'))

    return ret


def build_list_block(o, leadCnt=0, position=C._AS_VALUE_):
    ret = pstr('')

    tail = tail_symbol(position)

    '所有元素显示在同一行'
    if S.list_in_line:
        _f = map(lambda e: not (is_extendable(e) or too_long(leadCnt, position, e)), o)
        if all(_f):
            _o = map(lambda e: typeval(None, e), o)
            if S.newline or position & C._AS_ELEMENT_:
                ret += pstr(S.leading * leadCnt)
            ret += pstr("[") + ', '.join(_o) + pstr("]%s\n" % tail)
            return _b(ret)

    # [
    if S.newline or position & C._AS_ELEMENT_:
        ret += _b(S.leading * leadCnt + pstr('[\n'))
    else:
        ret += _b(pstr('[\n'))

    # body
    for e in o:
        ret += build_single_block(e, leadCnt + 1,
                                  C._AS_ELEMENT_ | C._AS_LIST_ELEMENT_)

    # ]
    ret += _b(S.leading * leadCnt + pstr(']%s\n' % tail))

    return ret


def build_tuple_block(o, leadCnt=0, position=C._AS_VALUE_):
    ret = pstr('')

    tail = tail_symbol(position)

    if S.tuple_in_line:
        _f = map(lambda e: not is_extendable(e), o)
        if all(_f):
            _o = map(lambda e: typeval(None, e), o)
            if S.newline or position & C._AS_ELEMENT_:
                ret += pstr(S.leading * leadCnt)
            ret += _b(pstr("(") + ', '.join(_o) + ')%s\n' % tail)
            return ret

    # (
    if S.newline or position & C._AS_ELEMENT_:
        ret += _b(S.leading * leadCnt + pstr('(\n'))
    else:
        ret += _b(pstr('(\n'))

    # body
    for e in o:
        ret += build_single_block(e, leadCnt + 1,
                                  C._AS_ELEMENT_ | C._AS_TUPLE_ELEMENT_)

    # )
    ret += _b(S.leading * leadCnt + pstr(')%s\n' % tail))

    return ret


def build_dict_block(o, leadCnt=0, position=C._AS_VALUE_):
    ret = pstr('')

    tail = tail_symbol(position)
    # {
    if S.newline or position & C._AS_ELEMENT_:
        ret += _b(S.leading * leadCnt + pstr('{') + pstr('\n'))
    else:
        ret += _b(pstr('{') + pstr('\n'))

    # body
    for k, v in o.items():
        # v = o[k]
        if dict_key_filter(o, k, v):
            continue
        # ret += S.leading*(leadCnt + 1) + typeval(k) + pstr(": ")
        # ret += build_single_block(v, leadCnt+1)
        ret += build_pair_block(k, v, leadCnt + 1, C._AS_DICT_ELEMENT_)

    # }
    ret += _b(S.leading * leadCnt + '}' + pstr(tail + u'\n'))

    return ret


def build_class_block(o, leadCnt=0, position=C._AS_ELEMENT_):
    debug(C._DL_FUNC_, leadCnt,
          ('obj:%s leadCnt:%s position:%d' \
           % (o, leadCnt, position)))
    ret = pstr('')

    tail = tail_symbol(position)

    # {
    _leading = pstr('')
    if position & C._AS_ELEMENT_:
        _leading += S.leading * leadCnt
    # elif position & C._AS_DICT_ELEMENT_:
    #     _leading += pstr(' ')
    elif position & C._AS_VALUE_:
        _leading += pstr('')

    if is_class_instance(o):
        ret += _b(_leading + pstr('instance(%s):' %
                                  o.__class__.__name__) + pstr('\n'))
    elif inspect.isfunction(o):
        ret += _b(_leading + pstr('function(%s):' % o.__name__) + pstr('\n'))
    elif inspect.isbuiltin(o):
        ret += _b(_leading + pstr('builtin(%s):' % o.__name__) + pstr('\n'))
    elif inspect.ismethod(o):
        ret += _b(_leading + pstr('method(%s):' % o.__name__) + pstr('\n'))
    else:
        '本身就是类，不是对象'
        try:
            ret += _b(_leading + pstr('class(%s):' % o.__name__) + pstr('\n'))
        except:
            print(inspect.isclass(o))
            print(o, dir(o))
            raise

    # body
    props = dir(o)
    props_cnt = len(props)
    filter_count = 0
    for idx, attr in enumerate(props):
        if attr == '__abstractmethods__':
            continue

        try:
            val = getattr(o, attr)
        except Exception as e:
            val = "<ERROR: CAN NOT ACCESS ATTRIBUTE. MESSAGE: %s>" % e
        '过滤不需要的属性'
        if object_attr_default_filter(o, attr, val):
            filter_count += 1
            continue

        '最后一个元素不需要再加(,)逗号'
        if idx == props_cnt - 1:
            position = C._AS_VALUE_
        else:
            position = C._AS_CLASS_ELEMENT_

        # '忽略掉 以__开头的成员、自引用成员、函数成员'
        ret += build_pair_block(attr,
                                val,
                                leadCnt + 1,
                                position | C._AS_CLASS_ELEMENT_)

    # }
    if filter_count == props_cnt:
        # right strip ':\n'
        ret = ret[:-2]
    else:
        # right strip ',\n' which belongs to last element of class
        ret = ret[:-2]

    ret += pstr(tail + u'\n')
    return ret



def is_newline_obj(o):
    if hasattr(o, '__module__'):
        return True
    return False


def is_class(o):
    try:
        # detect class
        # for py3, to detect both old-style and new-style class
        # for py2, to detect new-style class
        o.__flags__
        return True
    except:
        if inspect.isclass(o):
            return True
    return False


def is_class_instance(o):
    try:
        # to detect:
        # old-style class & new-style class
        # instance of old-style class and of new-style class
        # method of instance of both class
        # function

        # o.__module__ in python 3.5 some instance has no this attribute

        if (inspect.isclass(o)
            or inspect.isfunction(o)
            or inspect.ismethod(o)):
            return False
        return True
    except:
        pass
    return False
