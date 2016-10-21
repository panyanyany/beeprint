# -*- coding:utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division

from io import StringIO

import urwid
import inspect

from beeprint import utils
from beeprint import helper
from beeprint import constants as C
from beeprint.config import Config
from beeprint.debug_kit import debug
from beeprint.utils import (is_newline_obj, is_class_instance, pyv, 
                            _unicode, get_name, get_type, has_custom_repr,
                            is_base_type)
from beeprint.helper import (object_attr_default_filter, dict_key_filter, 
                             ustr, is_extendable)
from beeprint.lib import search_up_tree as sut
from beeprint.lib import position_dict
from beeprint.helpers.string import (break_string, 
                                     calc_width, calc_left_margin,
                                     too_long, shrink_inner_string,
                                     get_line_width, is_printable)
from beeprint.models.wrapper import StringWrapper


class Block(object):
    ctx = None
    ctn = None

    def __init__(self, config, ctx):
        self.config = config
        self.ctx = ctx
        self.ctx.element_ending = self.get_element_ending()
        self.ctn = BlockContent(self)

    def __str__(self):
        return self.build_block()

    def get_block_ending(self, value=None):
        ending = u'\n'
        if self.ctx.position & C._AS_VALUE_:
            ending = u''
        if self.ctx.position & C._AS_CLASS_ELEMENT_:
            'last element of class has no ending'
            elements = self.ctx.parent.get_elements()
            if elements.index(self.ctx.obj) == len(elements)-1:
                ending = u''
        return ending

    def get_element_ending(self, value=None):
        position = self.ctx.position
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
                elements = self.ctx.parent.get_elements()
                if elements.index(self.ctx.obj) == len(elements)-1:
                    tail = u''
            elif is_class_instance(value) or utils.is_class(value):
                if self.ctx.indent_cnt >= self.config.max_depth:
                    # if reach max depth, the value would be repr as one-line string
                    # so comma is need
                    pass
                else:
                    tail = u''
            # print('%s or %s: %s' % (is_class_instance(value), utils.is_class(value), value))

        return tail

    def get_elements(self):
        raise Exception("%s does not implement this method" % 
                        self.__class__)

    def build_block(self):
        """遍历对象，判断对象内成员的类型，然后构造对应的 *Block"""

        indent_cnt = self.ctx.indent_cnt
        obj = self.ctx.obj
        position = self.ctx.position

        debug(self.config, C._DL_FUNC_, 
              indent_cnt,
              ('obj:{} indent_cnt:{} position:{:b}'.format(
                  obj, indent_cnt, position)))

        ret = ustr('')

        tail = self.ctx.element_ending
        block_ending = self.get_block_ending()
        debug(self.config, C._DL_STATEMENT, 
              indent_cnt, 'tail, block_ending: ' + str([tail, block_ending]))

        # recursive check
        oid = id(obj)
        if oid in self.ctx.obj_ids:
            if self.config.newline or position & C._AS_ELEMENT_:
                ret = ustr(indent_cnt * self.config.indent_char)
            else:
                ret = ustr("")

            if is_base_type(obj):
                typename = '%s' % get_name(obj)
            else:
                typename = '%s(%s)' % (get_type(obj), get_name(obj))
            ret += ustr("<Recursion on %s with id=%d>" % (typename, oid))
            ret += tail + block_ending
            return self.ctn.write(ret)
        self.ctx.obj_ids = self.ctx.obj_ids.copy()
        self.ctx.obj_ids.add(oid)

        if self.config.max_depth <= indent_cnt:
            if self.config.newline or position & C._AS_ELEMENT_:
                ret = ustr(indent_cnt * self.config.indent_char)
            else:
                ret = ustr(" ")

            rb = ReprBlock(self.config, self.ctx, handlers=[
                ReprStringHandlerInlineRepr(self.config), 
                ReprOthersHandlerInlineRepr(self.config)])
            ret += str(rb) + tail + '\n'
            return self.ctn.write(ret)

        if isinstance(obj, dict):
            debug(self.config, C._DL_STATEMENT, indent_cnt, 'is dict')
            ret += str(DictBlock(self.config, self.ctx))
        elif isinstance(obj, list):
            debug(self.config, C._DL_STATEMENT, indent_cnt, 'is list')
            ret += str(ListBlock(self.config, self.ctx))
        elif isinstance(obj, tuple):
            debug(self.config, C._DL_STATEMENT, indent_cnt, 'is tuple')
            ret += str(TupleBlock(self.config, self.ctx))
        elif is_extendable(obj):
            debug(self.config, C._DL_STATEMENT, indent_cnt, 'is extendable')
            ret += str(ClassBlock(self.config, self.ctx))
        else:
            debug(self.config, C._DL_STATEMENT, indent_cnt, 'is simple type')
            rb = ReprBlock(self.config, self.ctx, handlers=[
                ReprStringHandlerMultiLiner(self.config), 
                ReprOthersHandler(self.config)])
            ret += self.ctn.write(indent_cnt * self.config.indent_char + str(rb) + ustr(tail + '\n'))

        return ret

class ClassBlock(Block):

    def get_elements(self):
        o = self.ctx.obj
        props = []
        for attr_name in dir(o):
            if attr_name == '__abstractmethods__':
                continue

            try:
                attr = getattr(o, attr_name)
            except Exception as e:
                continue

            if object_attr_default_filter(self.config, o, attr_name, attr):
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
        if len(self.get_elements()) > 0:
            return u''
        else:
            return super(self.__class__, self).get_element_ending()

    '''
    def get_block_ending(self):
        return u''
    '''

    def build_block(self):
        indent_cnt = self.ctx.indent_cnt
        o = self.ctx.obj
        position = self.ctx.position

        debug(self.config, C._DL_FUNC_, indent_cnt,
              ('obj:{} indent_cnt:{} position:{:b}'.format(
                  o, indent_cnt, position)))

        tail = self.ctx.element_ending
        block_ending = self.get_block_ending()
        debug(self.config, C._DL_STATEMENT, 
              indent_cnt, 'tail, block_ending: ' + str([tail, block_ending]))

        # {
        _leading = ustr('')
        if position & C._AS_ELEMENT_:
            _leading += self.config.indent_char * indent_cnt
        elif position & C._AS_VALUE_:
            _leading += ustr('')

        name = get_name(o)
        label = get_type(o)

        ret = _leading
        if (self.config.instance_repr_enable and 
                is_class_instance(self.ctx.obj) and
                has_custom_repr(self.ctx.obj)):
            ret = self.ctn.write(ret + ustr(repr(self.ctx.obj)))
        else:
            ret += '%s(%s):' % (label, name) + '\n'

            # body
            ele_ctnr = self.get_elements()
            props_cnt = len(ele_ctnr)

            if props_cnt == 0:
                # right strip ':\n'
                ret = ret[:-2]

            ret = self.ctn.write(ret)

            for idx, key, val in ele_ctnr:
                # '忽略掉 以__开头的成员、自引用成员、函数成员'
                ctx = self.ctx.clone()
                ctx.obj = (key, val)
                ctx.parent = self
                ctx.position = C._AS_CLASS_ELEMENT_
                ctx.indent_cnt = self.ctx.indent_cnt + 1
                ret += str(PairBlock(self.config, ctx))

        # }
        ret += self.ctn.write(tail + block_ending)
        return ret

class DictBlock(Block):

    def __init__(self, config, ctx):
        ctx.__dict__.setdefault('position', C._AS_VALUE_)
        super(self.__class__, self).__init__(config, ctx)

    def get_elements(self):
        if not self.config.dict_ordered_key_enable:
            return self.ctx.obj.items()

        def items(self):
            keys = list(self.ctx.obj.keys())
            try:
                keys.sort()
            except:
                # if keys elements are type() objects, it can not be sort
                keys.sort(key=lambda e: repr(e))
            for k in keys:
                yield k, self.ctx.obj[k]
        return items(self)

    def build_block(self):

        indent_cnt = self.ctx.indent_cnt
        o = self.ctx.obj
        position = self.ctx.position

        debug(self.config, C._DL_FUNC_, indent_cnt,
              ('obj:{} indent_cnt:{} position:{:b}'.format(
                  o, indent_cnt, position)))

        ret = ustr('')
        tail = self.ctx.element_ending
        block_ending = self.get_block_ending()
        debug(self.config, C._DL_STATEMENT, indent_cnt, 'tail, block_ending: ' + str([tail, block_ending]))
        # {
        if self.config.newline or position & C._AS_ELEMENT_:
            ret += self.ctn.write(self.config.indent_char * indent_cnt + ustr('{') + ustr('\n'))
        else:
            ret += self.ctn.write(ustr('{') + ustr('\n'))

        # body
        for k, v in self.get_elements():
            if dict_key_filter(o, k, v):
                continue
            ctx = self.ctx.clone()
            ctx.obj = (k, v)
            ctx.parent = self
            ctx.position = C._AS_DICT_ELEMENT_
            ctx.indent_cnt = self.ctx.indent_cnt + 1
            ret += str(PairBlock(self.config, ctx))

        # }
        ret += self.ctn.write(self.config.indent_char * indent_cnt + '}' + ustr(tail + block_ending))

        return ret

class ListBlock(Block):

    def __init__(self, config, ctx):
        ctx.__dict__.setdefault('position', C._AS_VALUE_)
        super(self.__class__, self).__init__(config, ctx)

    def get_elements(self):
        return self.ctx.obj

    def build_block(self):
        indent_cnt = self.ctx.indent_cnt
        o = self.ctx.obj
        position = self.ctx.position
        ret = ustr('')

        tail = self.ctx.element_ending
        block_ending = self.get_block_ending()
        debug(self.config, 
              C._DL_FUNC_, 
              indent_cnt, 'tail, block_ending: ' + str([tail, block_ending]))

        '所有元素显示在同一行'
        if self.config.list_in_line:
            _f = map(
                lambda e: (not (is_extendable(e) or 
                                too_long(self.config.indent_char, 
                                         indent_cnt, position, repr_block(e, self.config)))), 
                o)
            if all(_f):
                _o = map(lambda e: repr_block(e, self.config), o)
                if self.config.newline or position & C._AS_ELEMENT_:
                    ret += self.ctn.write(self.config.indent_char * indent_cnt)
                ret += self.ctn.write("[")
                for (i, e) in enumerate(_o):
                    if i:
                        ret += self.ctn.write(', ')
                    ret += self.ctn.write(e)
                ret +=  self.ctn.write("]" + tail + block_ending)
                return ret

        # [
        if self.config.newline or position & C._AS_ELEMENT_:
            ret += self.ctn.write(self.config.indent_char * indent_cnt + ustr('[') + ustr('\n'))
        else:
            ret += self.ctn.write(ustr('[') + ustr('\n'))

        # body
        for e in o:
            ctx = self.ctx.clone()
            ctx.obj = e
            ctx.parent = self
            ctx.indent_cnt = self.ctx.indent_cnt + 1
            ctx.position = C._AS_ELEMENT_ | C._AS_LIST_ELEMENT_
            ret += str(Block(self.config, ctx))

        # ]
        ret += self.ctn.write(self.config.indent_char * indent_cnt + ustr(']' + tail + block_ending))

        return ret



class TupleBlock(Block):

    def __init__(self, config, ctx):
        ctx.__dict__.setdefault('position', C._AS_VALUE_)
        super(self.__class__, self).__init__(config, ctx)

    def get_elements(self):
        return self.ctx.obj

    def build_block(self):
        indent_cnt = self.ctx.indent_cnt
        o = self.ctx.obj
        position = self.ctx.position

        debug(self.config, C._DL_FUNC_, 
              indent_cnt,
              ('obj:{} indent_cnt:{} position:{:b}'.format(
                  o, indent_cnt, position)))
        ret = ustr('')

        tail = self.ctx.element_ending
        block_ending = self.get_block_ending()
        debug(self.config, C._DL_STATEMENT, indent_cnt, 'tail, block_ending: ' + str([tail, block_ending]))

        if self.config.tuple_in_line:
            _f = map(lambda e: not is_extendable(e), o)
            if all(_f):
                _o = map(lambda e: repr_block(e, self.config), o)
                if self.config.newline or position & C._AS_ELEMENT_:
                    ret += self.ctn.write(self.config.indent_char * indent_cnt)
                ret += self.ctn.write(ustr("("))
                for (i, e) in enumerate(_o):
                    if i:
                        ret += self.ctn.write(', ')
                    ret += self.ctn.write(e)
                ret += self.ctn.write(')' + tail + block_ending)
                return ret

        # (
        if self.config.newline or position & C._AS_ELEMENT_:
            ret += self.ctn.write(self.config.indent_char * indent_cnt + ustr('(\n'))
        else:
            ret += self.ctn.write(ustr('(\n'))

        # body
        for e in self.get_elements():
            ctx = self.ctx.clone()
            ctx.obj = e
            ctx.parent = self
            ctx.position = C._AS_ELEMENT_ | C._AS_TUPLE_ELEMENT_
            ctx.indent_cnt += 1
            ret += str(Block(self.config, ctx))

        # )
        ret += self.ctn.write(self.config.indent_char * indent_cnt + ustr(')' + tail + block_ending))

        return ret

class PairBlock(Block):

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.ctx.key = self.ctx.obj[0]
        self.ctx.key_expr = self.get_key(self.ctx.position, self.ctx.key)

    def get_key(self, position, name):
        if position & C._AS_CLASS_ELEMENT_:
            # class method name or attribute name no need to add u or b prefix
            key = ustr(name)
        else:
            key = repr_block(name, self.config)

        return key

    def get_element_ending(self, value=None):
        value = value or self.ctx.obj[1]
        return super(self.__class__, self).get_element_ending(value)


    def build_block(self):
        indent_cnt = self.ctx.indent_cnt
        name, val = self.ctx.obj
        position = self.ctx.position

        debug(self.config, C._DL_FUNC_, indent_cnt,
              ('key:{}, indent_cnt:{}, position:{:b}'.format(
                  name, indent_cnt, position)))
        ret = ustr('')

        tail = self.ctx.element_ending
        block_ending = self.get_block_ending(val)
        debug(self.config, C._DL_STATEMENT, 
              indent_cnt, 'tail, block_ending: ' + str([tail, block_ending]))

        key = self.ctx.key_expr

        ret += self.ctn.write(self.config.indent_char * indent_cnt + key + ':')
        if is_extendable(val) and self.config.max_depth > indent_cnt:
            # still in of range, and can be expanded

            # value need to be dispalyed on new line
            # including: 
            #   class type & class instance
            #   function type
            if self.config.newline or (is_newline_obj(val) and
                                 position & C._AS_ELEMENT_):
                ret += self.ctn.write(ustr('\n'))
                indent_cnt = indent_cnt + 1
                position = C._AS_ELEMENT_
                debug(self.config, C._DL_STATEMENT, indent_cnt, 'make newline')
            # value will be dispalyed immediately after one space
            else:
                ret += self.ctn.write(ustr(" "))
                position = C._AS_VALUE_

            ctx = self.ctx.clone()
            ctx.obj = val
            ctx.parent = self
            ctx.position =  position
            ctx.indent_cnt = indent_cnt
            ret += str(Block(self.config, ctx))
            ret += self.ctn.write(tail + block_ending)
        else:
            ctx = self.ctx.clone()
            ctx.obj = val
            if self.config.max_depth <= indent_cnt:
                # reach max_depth, just show brief message
                rb = ReprBlock(self.config, ctx, 
                               handlers=[ReprStringHandlerInlineRepr(self.config), 
                                         ReprOthersHandlerInlineRepr(self.config)])
                ret += self.ctn.write(ustr(" " + str(rb) + tail + block_ending))
            else:
                rb = ReprBlock(self.config, ctx, 
                               handlers=[ReprStringHandlerMultiLiner(self.config), 
                                         ReprOthersHandler(self.config)])
                ret += self.ctn.write(ustr(" ") + str(rb) + ustr(tail + block_ending))

        return ret


class Context(object):
    """Context contains info of current line displaying,
    it tells you where you are in the whole block
    it tells you what happened before on the same line
    it tells you what **will** happened after you on the same line
    """

    def __init__(self, **attrs):
        # must explicitly set attributes to instance
        # or below attribute will always be set as C._AS_VALUE_:
        #
        #   ctx.__dict__.setdefault('position', C._AS_VALUE_)
        #
        # which will always override the default value C._AS_ELEMENT_

        self.obj = None
        self.parent = None

        self.indent_char = Config.indent_char
        self.position = C._AS_ELEMENT_
        self.indent_cnt = 0

        self.seperator = ":"
        self.after_seperator = " "

        self.element_ending = None
        self.key = None
        self.key_expr = ''

        self.obj_ids = set()

        self.__dict__.update(**attrs)

    def clone(self):
        ctx = self.__class__(**self.__dict__)
        return ctx

    @property
    def indent(self):
        return self.indent_char*self.indent_cnt

    @property
    def sep_expr(self):
        if self.key is None:
            return ''
        return self.seperator + u' '

    @property
    def val_expr(self):
        raise Exception("not yet implement")


def repr_block(obj, config=Config()):
    return str(ReprBlock(config, Context(obj=obj)))


class ReprBlock(Block):
    """like repr(), but provides more functions"""

    def __init__(self, config, ctx, handlers=None):
        self.config = config
        self.ctx = ctx
        self.handlers = handlers or [
            ReprStringHandler(self.config), 
            ReprOthersHandler(self.config)]
        self.typ = ReprBlock.ReprType(ctx.obj)

    def build_block(self):
        for handler in self.handlers:
            if handler.accept(self.typ):
                return handler(self.ctx, self.typ)

        raise Exception("no handlers")

    class Handler(object):

        def __init__(self, config):
            self.config = config
        
        def accept(self, typ):
            raise Exception("Unimplement method")

        def __call__(self, ctx, typ):
            raise Exception("Unimplement method")
    
    class ReprType(object):

        _LITERAL_ = 1 # string literal depends on script's coding
        _UNICODE_ = 2
        _BYTES_ = 4
        _OTHERS_ = 8

        typ = 0

        def __init__(self, obj):
            self.typ = self.judge(obj)

        def is_all(self, *args):
            bi_ands = map(lambda b: b & self.typ, args)
            return all(bi_ands)

        def is_any(self, *args):
            bi_ands = map(lambda b: b & self.typ, args)
            return any(bi_ands)

        def is_string(self):
            return self.is_any(
                self.__class__._LITERAL_,
                self.__class__._UNICODE_,
                self.__class__._BYTES_,
            )

        @classmethod
        def judge(cls, obj):
            if pyv == 2:
                # in py2, string literal is both instance of str and bytes
                # a literal string is str (i.e: coding encoded, eg: utf8)
                # a u-prefixed string is unicode
                if isinstance(obj, _unicode):
                    return cls._UNICODE_
                elif isinstance(obj, str):  # same as isinstance(v, bytes)
                    return cls._LITERAL_ | cls._BYTES_
            else:
                # in py3, 
                # a literal string is str (i.e: unicode encoded)
                # a u-prefixed string is str
                # a utf8 string is bytes
                if isinstance(obj, bytes):
                    return cls._BYTES_
                elif isinstance(obj, str):
                    return cls._LITERAL_ | cls._UNICODE_

            return cls._OTHERS_


class ReprStringHandler(ReprBlock.Handler):
    """handle repr while processing string object like unicode, bytes, str"""

    def __init__(self, *args, **kwargs):
        # whether to quote the string
        self.do_quote = kwargs.pop('do_quote', None) or True
        super(ReprStringHandler, self).__init__(*args, **kwargs)

    def accept(self, typ):
        return typ.is_string()

    def escape(self, obj, typ):
        obj = obj.replace(u'\\', u'\\\\')
        obj = obj.replace(u'\n', u'\\n')
        obj = obj.replace(u'\r', u'\\r')
        obj = obj.replace(u'\t', u'\\t')

        return obj

    def __call__(self, ctx, typ):
        if typ.is_all(typ._BYTES_):
            if pyv == 2:
                # convert to unicode
                ctx.obj = ctx.obj.decode(self.config.encoding, 'replace')
                ctx.obj = self.escape(ctx.obj, typ)
            else:
                ctx.obj = repr(ctx.obj)[2:-1]
        else:
            sio = StringIO()
            for char in ctx.obj:
                if is_printable(char):
                    char = self.escape(char, typ)
                    sio.write(char)
                else:
                    char = repr(char)[1:-1]
                    if pyv == 2:
                        char = char[1:]
                        char = char.decode(self.config.encoding)
                    sio.write(char)
            ctx.obj = sio.getvalue()
            sio.close()
            """
            try:
                ctx.obj.encode('utf8')
                ctx.obj = self.escape(ctx.obj, typ)
            except:
                ctx.obj = repr(ctx.obj)[1:-1]
            """

        if self.do_quote:
            wrapper = StringWrapper(self.config, typ)
        else:
            wrapper = StringWrapper(self.config, typ, lqm='', rqm='')

        return self.rearrenge(ctx, typ, wrapper)

    def rearrenge(self, ctx, typ, wrapper):
        return wrapper.wrap(ctx.obj)

class ReprStringHandlerMultiLiner(ReprStringHandler):

    def rearrenge(self, ctx, typ, wrapper):
        assert ctx.element_ending is not None, "element_ending must be set"

        left_margin = calc_left_margin(ctx, wrapper)
        # calculate availiable width for string
        a_width = get_line_width(self.config.string_break_method,
                                 self.config.string_break_width) - left_margin

        if a_width > 0:
            seg_list = break_string(
                ctx.obj + 
                wrapper.rqm + 
                ctx.element_ending, 
                a_width)

            seg_list[-1] = seg_list[-1].rstrip(
                wrapper.rqm + 
                ctx.element_ending,
            )
            indent_char_width = calc_width(self.config.indent_char)
            left_margin_chars = (left_margin // indent_char_width * self.config.indent_char + 
                                 left_margin % indent_char_width * ' ')
            for i in range(1, len(seg_list)):
                seg_list[i] = ''.join([
                    left_margin_chars,
                    seg_list[i],
                ])

            if (self.config.text_autoclip_enable and 
                    self.config.text_autoclip_method == C._TEXT_AUTOCLIP_BY_LINE):
                lines_cnt = len(seg_list)
                if lines_cnt > self.config.text_autoclip_maxline:
                    seg_list = seg_list[:self.config.text_autoclip_maxline]
                    hidden_lines = lines_cnt - self.config.text_autoclip_maxline
                    plural_sign = '' if hidden_lines == 1 else 's'
                    seg_list.append("%s...(%d hidden line%s)" % (left_margin_chars, hidden_lines, plural_sign))
            ctx.obj = "\n".join(seg_list)

        return wrapper.wrap(ctx.obj)


class ReprOthersHandler(ReprBlock.Handler):

    def accept(self, typ):
        return not typ.is_string()

    def __call__(self, ctx, typ):
        return ustr(repr(ctx.obj))


class ReprStringHandlerInlineRepr(ReprStringHandler):
    """repr string object in one line"""

    def rearrenge(self, ctx, typ, wrapper):
        shrink_inner_string(ctx, 
                            self.config.string_break_method,
                            self.config.string_break_width,
                            wrapper)
        return wrapper.wrap(ctx.obj)


class ReprOthersHandlerInlineRepr(ReprOthersHandler):
    """repr non-string object in one line"""
    
    def __call__(self, ctx, typ):
        ctx.obj = ustr(repr(ctx.obj))
        shrink_inner_string(ctx, 
                            self.config.string_break_method,
                            self.config.string_break_width,
                            None)

        return ctx.obj


class BlockContent(object):

    def __init__(self, blk):
        self.blk = blk
        self.str = ''

    def write(self, s):
        self.str += s
        config = self.blk.config
        if config and config.stream:
            config.stream.write(s)
            config.stream.flush()
        return s

    def puts(self, s):
        s += '\n'
        return self.write(s)

    def count_lines(self):
        return self.str.count('\n')
