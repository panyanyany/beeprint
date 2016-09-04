# -*- coding:utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division

import urwid
import inspect

from beeprint import utils
from beeprint import helper
from beeprint import settings as S
from beeprint import constants as C
from beeprint.debug_kit import debug
from beeprint.utils import is_newline_obj, is_class_instance
from beeprint.helper import object_attr_default_filter, dict_key_filter, tail_symbol, _b
from beeprint.helper import ustr, tail_symbol, is_extendable
from beeprint.lib import search_up_tree as sut
from beeprint.lib import position_dict
from beeprint.models import st_handler 
from beeprint.helpers.block import pair_block_key


class Block(object):
    parent = None
    position = 0
    indent_cnt = 0
    subject = None

    def __init__(self, subj, parent=None, position=C._AS_ELEMENT_, indent=0):
        self.subject = subj
        self.parent = parent
        self.position = position
        self.indent_cnt = indent

    def __str__(self):
        return self.build_block()

    def get_block_ending(self, value=None):
        ending = u'\n'
        if self.position & C._AS_VALUE_:
            ending = u''
        if self.position & C._AS_CLASS_ELEMENT_:
            'last element of class has no ending'
            elements = self.parent.get_elements()
            if elements.index(self.subject) == len(elements)-1:
                ending = u''
        return ending

    def get_element_ending(self, value=None):
        position = self.position
        tail = u''
        if position & C._AS_VALUE_:
            tail = u''
        elif (position & C._AS_LIST_ELEMENT_ or
                position & C._AS_DICT_ELEMENT_ or
                position & C._AS_CLASS_ELEMENT_ or
                position & C._AS_TUPLE_ELEMENT_):
            tail = u','

            if False:
                pass
            elif position & C._AS_CLASS_ELEMENT_:
                'last element of class has no ending'
                elements = self.parent.get_elements()
                if elements.index(self.subject) == len(elements)-1:
                    tail = u''
            elif is_class_instance(value) or utils.is_class(value):
                tail = u''
            # print('%s or %s: %s' % (is_class_instance(value), utils.is_class(value), value))

        return tail

    def get_elements(self):
        raise Exception("%s does not implement this method" % 
                        self.__class__)

    def build_block(self):
        """遍历对象，判断对象内成员的类型，然后构造对应的 *Block"""

        leadCnt = self.indent_cnt
        obj = self.subject
        position = self.position

        debug(C._DL_FUNC_, 
              leadCnt,
              ('obj:{} leadCnt:{} position:{:b}'.format(
                  obj, leadCnt, position)))

        ret = ustr('')

        tail = self.get_element_ending()
        block_ending = u''
        debug(C._DL_STATEMENT, leadCnt, 'tail, block_ending: ' + str([tail, block_ending]))

        if S.max_depth <= leadCnt:
            context = Context(indent_char=S.leading, 
                              position=position, 
                              lead_cnt=leadCnt,
                              element_tail=tail)
            imsg = st_handler.inline_msg(obj, context)
            if S.newline or position & C._AS_ELEMENT_:
                ret = ustr(leadCnt * S.leading) + imsg + ustr("\n")
            else:
                ret = ustr(" ") + imsg + ustr("\n")
            if position & C._AS_LIST_ELEMENT_:
                ret = ret[:-1] + ustr(tail + "\n")
            return _b(ret)

        if isinstance(obj, dict):
            debug(C._DL_STATEMENT, leadCnt, 'is dict')
            ret += str(DictBlock(obj, self.parent, position=position, indent=leadCnt))
        elif isinstance(obj, list):
            debug(C._DL_STATEMENT, leadCnt, 'is list')
            ret += str(ListBlock(obj, self.parent, position=position, indent=leadCnt))
        elif isinstance(obj, tuple):
            debug(C._DL_STATEMENT, leadCnt, 'is tuple')
            ret += str(TupleBlock(obj, self.parent, position=position, indent=leadCnt))
        elif is_extendable(obj):
            debug(C._DL_STATEMENT, leadCnt, 'is extendable')
            ret += str(ClassBlock(obj, self.parent, position=position, indent=leadCnt))
        else:
            debug(C._DL_STATEMENT, leadCnt, 'is simple type')
            context = Context(indent_char=S.leading, 
                              position=position, 
                              lead_cnt=leadCnt,
                              element_tail=tail)
            ret += _b(leadCnt * S.leading + st_handler.typeval_b(obj, context) + ustr(tail + '\n'))

        return ret

class ClassBlock(Block):

    props = None

    def get_elements(self):
        o = self.subject
        props = []
        for attr_name in dir(o):
            if attr_name == '__abstractmethods__':
                continue

            try:
                attr = getattr(o, attr_name)
            except Exception as e:
                continue

            if object_attr_default_filter(o, attr_name, attr):
                continue

            props.append((attr_name, attr))

        return position_dict.PositionDict(props)

    def get_element_ending(self):
        """A class block would have many nested elements,
        it would not know how its children respresent.
        for example: 

        Example One:
        >>> class(A):
        ...   class(B),

        Example Two:
        >>> class(A):
        ...   class(B):
        ...     prop: val

        As above, class(A) does not know and **should not know** whether class(B) has children
        
        So, the block of class(A) only need to do is just to add a newline to finish itself.
        """
        return u''

    '''
    def get_block_ending(self):
        return u''
    '''

    def build_block(self):
        leadCnt = self.indent_cnt
        o = self.subject
        position = self.position

        debug(C._DL_FUNC_, leadCnt,
              ('obj:{} leadCnt:{} position:{:b}'.format(
                  o, leadCnt, position)))

        ret = ustr('')

        tail = self.get_element_ending()
        block_ending = self.get_block_ending()
        debug(C._DL_STATEMENT, leadCnt, 'tail, block_ending: ' + str([tail, block_ending]))

        # {
        _leading = ustr('')
        if position & C._AS_ELEMENT_:
            _leading += S.leading * leadCnt
        # elif position & C._AS_DICT_ELEMENT_:
        #     _leading += ustr(' ')
        elif position & C._AS_VALUE_:
            _leading += ustr('')

        if is_class_instance(o):
            ret += _b(_leading + ustr('instance(%s):' %
                                      o.__class__.__name__) + ustr('\n'))
        elif inspect.isfunction(o):
            ret += _b(_leading + ustr('function(%s):' % o.__name__) + ustr('\n'))
        elif inspect.isbuiltin(o):
            ret += _b(_leading + ustr('builtin(%s):' % o.__name__) + ustr('\n'))
        elif inspect.ismethod(o):
            ret += _b(_leading + ustr('method(%s):' % o.__name__) + ustr('\n'))
        else:
            '本身就是类，不是对象'
            try:
                ret += _b(_leading + ustr('class(%s):' % o.__name__) + ustr('\n'))
            except:
                print(inspect.isclass(o))
                print(o, dir(o))
                raise

        # body
        ele_ctnr = self.get_elements()

        props_cnt = len(ele_ctnr)
        for idx, key, val in ele_ctnr:
            '''
            '最后一个元素不需要再加(,)逗号'
            if idx == props_cnt - 1:
                position = C._AS_VALUE_
            else:
                position = C._AS_CLASS_ELEMENT_
            '''

            # '忽略掉 以__开头的成员、自引用成员、函数成员'
            ret += str(PairBlock((key, val),
                                 self, 
                                 position=C._AS_CLASS_ELEMENT_,
                                 indent=leadCnt + 1))

        # }
        if props_cnt == 0:
            # right strip ':\n'
            ret = ustr(ret[:-2] + u',\n')
        else:
            ret += ustr(tail + block_ending)
        return ret

class DictBlock(Block):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('position', C._AS_VALUE_)
        super(DictBlock, self).__init__(*args, **kwargs)

    def build_block(self):

        leadCnt = self.indent_cnt
        o = self.subject
        position = self.position

        debug(C._DL_FUNC_, leadCnt,
              ('obj:{} leadCnt:{} position:{:b}'.format(
                  o, leadCnt, position)))

        ret = ustr('')
        tail = self.get_element_ending()
        block_ending = self.get_block_ending()
        debug(C._DL_STATEMENT, leadCnt, 'tail, block_ending: ' + str([tail, block_ending]))
        # {
        if S.newline or position & C._AS_ELEMENT_:
            ret += _b(S.leading * leadCnt + ustr('{') + ustr('\n'))
        else:
            ret += _b(ustr('{') + ustr('\n'))

        # body
        for k, v in o.items():
            # v = o[k]
            if dict_key_filter(o, k, v):
                continue
            ret += str(PairBlock((k, v),
                                 self, 
                                 position=C._AS_DICT_ELEMENT_,
                                 indent=leadCnt + 1))

        # }
        ret += _b(S.leading * leadCnt + '}' + ustr(tail + block_ending))

        return ret

class ListBlock(Block):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('position', C._AS_VALUE_)
        super(ListBlock, self).__init__(*args, **kwargs)

    def build_block(self):
        leadCnt = self.indent_cnt
        o = self.subject
        position = self.position
        ret = ustr('')

        tail = self.get_element_ending()
        block_ending = self.get_block_ending()
        debug(C._DL_STATEMENT, leadCnt, 'tail, block_ending: ' + str([tail, block_ending]))

        '所有元素显示在同一行'
        if S.list_in_line:
            _f = map(lambda e: not (is_extendable(e) or st_handler.too_long(leadCnt, position, e)), o)
            if all(_f):
                _o = map(lambda e: st_handler.typeval(e), o)
                if S.newline or position & C._AS_ELEMENT_:
                    ret += ustr(S.leading * leadCnt)
                ret += ustr("[") + ', '.join(_o) + ustr("]" + tail + block_ending)
                return _b(ret)

        # [
        if S.newline or position & C._AS_ELEMENT_:
            ret += _b(S.leading * leadCnt + ustr('[') + ustr('\n'))
        else:
            ret += _b(ustr('[') + ustr('\n'))

        # body
        for e in o:
            ret += str(Block(e, self, 
                             position=C._AS_ELEMENT_ | C._AS_LIST_ELEMENT_,
                             indent=leadCnt + 1,
                             ))

        # ]
        ret += _b(S.leading * leadCnt + ustr(']' + tail + block_ending))

        return ret



class TupleBlock(Block):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('position', C._AS_VALUE_)
        super(TupleBlock, self).__init__(*args, **kwargs)

    def get_elements(self):
        return self.subject

    def build_block(self):
        leadCnt = self.indent_cnt
        o = self.subject
        position = self.position

        debug(C._DL_FUNC_, 
              leadCnt,
              ('obj:{} leadCnt:{} position:{:b}'.format(
                  o, leadCnt, position)))
        ret = ustr('')

        tail = self.get_element_ending()
        block_ending = self.get_block_ending()
        debug(C._DL_STATEMENT, leadCnt, 'tail, block_ending: ' + str([tail, block_ending]))

        if S.tuple_in_line:
            _f = map(lambda e: not is_extendable(e), o)
            if all(_f):
                _o = map(lambda e: st_handler.typeval(e), o)
                if S.newline or position & C._AS_ELEMENT_:
                    ret += ustr(S.leading * leadCnt)
                ret += _b(ustr("(") + ', '.join(_o) + ')' + tail + block_ending)
                return ret

        # (
        if S.newline or position & C._AS_ELEMENT_:
            ret += _b(S.leading * leadCnt + ustr('(\n'))
        else:
            ret += _b(ustr('(\n'))

        # body
        for e in self.get_elements():
            ret += str(Block(e, 
                             self,
                             position=C._AS_ELEMENT_ | C._AS_TUPLE_ELEMENT_,
                             indent=leadCnt + 1,
                             ))

        # )
        ret += _b(S.leading * leadCnt + ustr(')' + tail + block_ending))

        return ret

class PairBlock(Block):

    def build_block(self):
        leadCnt = self.indent_cnt
        name, val = self.subject
        position = self.position

        debug(C._DL_FUNC_, leadCnt,
              ('key:{}, leadCnt:{}, position:{:b}'.format(
                  name, leadCnt, position)))
        ret = ustr('')

        tail = self.get_element_ending(val)
        block_ending = self.get_block_ending(val)
        debug(C._DL_STATEMENT, leadCnt, 'tail, block_ending: ' + str([tail, block_ending]))

        key = pair_block_key(position, name)

        ret += _b(S.leading * leadCnt + key + ':')
        if is_extendable(val) and S.max_depth > leadCnt:
            # value need to be dispalyed on new line
            # including: 
            #   class type & class instance
            #   function type
            if S.newline or (is_newline_obj(val) and
                                 position & C._AS_ELEMENT_):
                ret += _b(ustr('\n'))
                leadCnt = leadCnt + 1
                # position &= ~C._AS_VALUE_
                # position |= C._AS_ELEMENT_
                position = C._AS_ELEMENT_
                debug(C._DL_STATEMENT, leadCnt, 'make newline')
            # value will be dispalyed immediately after one space
            else:
                ret += _b(ustr(" "))
                # position &= ~C._AS_ELEMENT_
                # position |= C._AS_VALUE_
                position = C._AS_VALUE_

            ret += str(Block(val, self, position=position, indent=leadCnt)) + ustr(tail + block_ending)
        else:
            context = Context(indent_char=S.leading, 
                              position=position, 
                              lead_cnt=leadCnt, 
                              key=name,
                              element_tail=tail)
            if S.max_depth <= leadCnt:
                ret += _b(ustr(" " + st_handler.inline_msg(val, context) + tail + block_ending))
            else:
                ret += _b(ustr(" ") + st_handler.typeval_b(val, context) + ustr(tail + block_ending))

        return ret


class Context(object):
    """Context contains info of current line displaying,
    it tells you where you are in the whole block
    it tells you what happened before on the same line
    it tells you what **will** happened after you on the same line
    """

    left_quoter = "'"
    right_quoter = "'"

    seperator = ":"
    after_seperator = " "

    def __init__(self, indent_char=None, position=None, lead_cnt=None, key=None, value=None, element_tail=None):

        self.indent_char = indent_char
        self.position = position
        self.lead_cnt = lead_cnt
        self.key = key
        self.value = value
        self.element_tail = element_tail

        self.value_left_brace = None
        self.value_right_brace = None

    @staticmethod
    def from_block(cls, indent_char, block, key=None, value=None):
        return cls(indent_char=indent_char, 
                   position=block.position,
                   lead_cnt=block.indent_cnt,
                   key=key,
                   value=value,
                   element_tail=block.get_element_ending())

    @property
    def leading(self):
        return self.indent_char*self.lead_cnt

    @property
    def key_expr(self):
        if self.key is None:
            return ''
        return pair_block_key(self.position, self.key)

    @property
    def sep_expr(self):
        if self.key is None:
            return ''
        return self.seperator + u' '

    @property
    def val_expr(self):
        raise Exception("not yet implement")

    def calc_wrapped_line_indent(self):
        leading = u''.join([
            self.leading,
            self.key_expr,
            self.sep_expr,
        ])
        indent = urwid.str_util.calc_width(leading, 0, len(leading))
        return indent


class StringEncloser(object):

    def __init__(self, body, lqm=u'\'', rqm=u'\''):
        self.string_type_mark = u''
        self.body = body
        self.left_quotation_mark = lqm
        self.right_quotation_mark = rqm

    def set_string_type_mark(self, mark):
        self.string_type_mark = mark

    def __str__(self):
        return ''.join([
            self.string_type_mark,
            self.left_quotation_mark,
            self.body,
            self.right_quotation_mark,
        ])


