# -*- coding:utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
import sys
import traceback
import types

if sys.version_info < (3, 0):
    # avoid throw [UnicodeEncodeError: 'ascii' codec can't encode characters]
    # exceptions, without these lines, the sys.getdefaultencoding() returns ascii
    from imp import reload
    reload(sys)
    sys.setdefaultencoding('utf-8')

    pyv = 2
else:
    unicode = str
    pyv = 3

from . import settings as S
from . import constants as C
from .debug_kit import debug


def object_attr_default_filter(obj, name, val):
    '过滤不需要的对象属性'

    for propLeading in S.prop_leading_filters:
        if name.startswith(propLeading):
            return True

    for prop in S.prop_filters:
        # filter is a type
        if type(prop) == types.TypeType:
            if type(val) == prop:
                return True
        # filter is a string
        elif isinstance(prop, basestring) or isinstance(prop, str):
            if name == prop:
                return True
        # filter is callable
        elif hasattr(prop, '__call__'):
            return prop(name, val)

    return False


def dict_key_filter(obj, name, val):
    return False


def _b(s):
    if S.write_to_buffer_when_execute:
        S.bufferHandle.write(s)
        S.bufferHandle.flush()
    return s

def pstr(s):
    '''convert all string to unicode
    for unicode is python's built-in coding
    '''
    res = u''

    if isinstance(s, unicode):
        res += s
    elif isinstance(s, str):
        # in python 2/3, it's utf8
        # so decode to unicode
        res += s.decode(S.encoding)
    else:
        res += str(s)#.decode(S.encoding)

    return res

def beeprint(o, output=True):

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


def print_exc_plus():
    """
    Print the usual traceback information, followed by a listing of all the
    local variables in each frame.
    """
    tb = sys.exc_info()[2]
    while 1:
        if not tb.tb_next:
            break
        tb = tb.tb_next
    stack = []
    f = tb.tb_frame
    while f:
        stack.append(f)
        f = f.f_back
    stack.reverse()
    traceback.print_exc()
    print("Locals by frame, innermost last")
    for frame in stack:
        print()
        print("Frame %s in %s at line %s" % (frame.f_code.co_name,
                                             frame.f_code.co_filename,
                                             frame.f_lineno))
        for key, value in frame.f_locals.items():
            print("\t%20s = " % key, end='')
            #We have to be careful not to cause a new error in our error
            #printer! Calling str() on an unknown object could cause an
            #error we don't want.
            try:
                print(value)
            except:
                print("<ERROR WHILE PRINTING VALUE>")


def tail_symbol(position):
    if (position & C._AS_LIST_ELEMENT_ or
            position & C._AS_DICT_ELEMENT_ or
            position & C._AS_CLASS_ELEMENT_ or
            position & C._AS_TUPLE_ELEMENT_):
        tail = ','
    else:
        tail = ''
    return tail


def build_single_block(obj, leadCnt=0, position=C._AS_ELEMENT_):
    '遍历对象，判断对象内成员的类型，然后调用对应的 build_*_block() 处理'

    debug(0, leadCnt, 'ready to build %s:%s' % (type(obj), obj))

    ret = pstr('')

    tail = tail_symbol(position)

    if S.maxDeep < leadCnt:
        if S.newline or position & C._AS_ELEMENT_:
            ret = pstr(leadCnt * S.leading) + pstr("<OUT OF RANGE>\n")
        else:
            ret = pstr(" ") + pstr("<OUT OF RANGE>\n")
        if position & C._AS_LIST_ELEMENT_:
            ret = ret[:-1] + pstr(tail + "\n")
        return _b(ret)

    if isinstance(obj, dict):
        debug(0, leadCnt, 'is dict')
        ret += build_dict_block(obj, leadCnt, position)
    elif isinstance(obj, list):
        debug(0, leadCnt, 'is list')
        ret += build_list_block(obj, leadCnt, position)
    elif isinstance(obj, tuple):
        debug(0, leadCnt, 'is tuple')
        ret += build_tuple_block(obj, leadCnt, position)
    # hasattr(obj, '__dict__') or isinstance(obj, object):
    elif is_extendable(obj):
        debug(0, leadCnt, 'is extendable')
        ret += build_class_block(obj, leadCnt, position)
    else:
        debug(0, leadCnt, 'is simple type')
        ret += _b(leadCnt * S.leading + typeval(obj) + pstr(tail + '\n'))

    return ret


def is_extendable(obj):
    '判断obj是否可以展开'
    return isinstance(obj, dict) or hasattr(obj, '__dict__') or isinstance(obj, (tuple, list, types.FrameType))


def build_pair_block(name, val, leadCnt=0, position=C._AS_ELEMENT_):
    ret = pstr('')

    tail = tail_symbol(position)

    ret += _b(S.leading * leadCnt + typeval(name) + ':')
    if is_extendable(val) and S.maxDeep > leadCnt:
        if S.newline or isinstance(val, (types.InstanceType, types.FunctionType)):
            ret += _b(pstr('\n'))
            leadCnt = leadCnt + 1
        else:
            ret += _b(pstr(" "))

        ret += build_single_block(val, leadCnt, C._AS_VALUE_)
    else:
        if S.maxDeep <= leadCnt:
            ret += _b(pstr(" <OUT OF RANGE>%s\n" % tail))
        else:
            ret += _b(pstr(" ") + typeval(val) + pstr(tail + '\n'))
    return ret


def build_string_block(s, leadCnt=0):
    return _b(leadCnt * S.leading + typeval(s) + pstr('\n'))


def build_list_block(o, leadCnt=0, position=C._AS_VALUE_):
    ret = pstr('')

    tail = tail_symbol(position)

    '所有元素显示在同一行'
    if S.list_in_line:
        _f = map(lambda e: not is_extendable(e), o)
        if all(_f):
            _o = map(lambda e: typeval(e), o)
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
            _o = map(lambda e: typeval(e), o)
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
    for k in o:
        v = o[k]
        if dict_key_filter(o, k, v):
            continue
        #ret += S.leading*(leadCnt + 1) + typeval(k) + pstr(": ")
        #ret += build_single_block(v, leadCnt+1)
        ret += build_pair_block(k, v, leadCnt + 1)

    # }
    ret += _b(S.leading * leadCnt + '}' + pstr(tail + '\n'))

    return ret


def build_class_block(o, leadCnt=0, position=C._AS_ELEMENT_):
    ret = pstr('')

    # {
    _leading = S.leading * leadCnt

    if hasattr(o, '__class__'):
        ret += _b(_leading + pstr('object(%s):' %
                                  o.__class__.__name__) + pstr('\n'))
    else:
        '本身就是类，不是对象'
        ret += _b(_leading + pstr('class(%s):' % o.__name__) + pstr('\n'))

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

        #'忽略掉 以__开头的成员、自引用成员、函数成员'
        ret += build_pair_block(attr, val, leadCnt + 1, position)

    ret += pstr((leadCnt + 1) * S.leading) + \
        pstr("<filter %d props>\n" % filter_count)

    # }
    #ret += S.leading*leadCnt + '}' + pstr('\n')
    return ret


def typeval(v):
    try:
        st = string_type(v)
        ret = u''
        if st == C.ST_LITERAL:
            ret = u'"' + pstr(v) + u'"'
        elif st == C.ST_UNICODE:
            ret = u"u'" + v + u"'"
        elif st == C.ST_BYTES:
            # in py3, printed string will enclose with b''
            ret = pstr(v)
        else:
            ret = pstr(v)

        ret = ret.replace(u'\n', u'\\n')
        ret = ret.replace(u'\r', u'\\r')

    except Exception as e:
        if S.priority_strategy == C._PS_CORRECTNESS_FIRST:
            print_exc_plus()
            raise e
        # S.priority_strategy == C._PS_CONTENT_FIRST:
        hx = v.decode("latin-1").encode("hex")
        ret = pstr("<CAN NOT PARSE OBJECT(hex:" + hx + "):" + str(e) + ">")

    return ret


def string_type(s):

    if pyv == 2:
        # in py2, string literal is both instance of str and bytes
        # a literal string is str
        # a utf8 string is str
        # a u-prefixed string is unicode
        if isinstance(s, unicode):
            return C.ST_UNICODE
        elif isinstance(s, str): # same as isinstance(v, bytes)
            return C.ST_LITERAL
    else:
        # in py3, 
        # a literal string is str
        # a u-prefixed string is str
        # a utf8 string is bytes
        if isinstance(s, bytes):
            return C.ST_BYTES
        elif isinstance(s, str):
            return C.ST_LITERAL
