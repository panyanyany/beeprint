# -*- coding:utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division

from beeprint import constants as C
from beeprint import settings as S
from beeprint import helper
from beeprint.utils import pyv, _unicode
from beeprint.helper import calc_width, cut_string
from beeprint.terminal_size import get_terminal_size


class StHandler(object):

    def __call__(self, obj, stype, context=None):
        self.obj = obj
        self.stype = stype
        self.context = context

        return self.handle()


class StUndefinedHandler(StHandler):

    def handle(self):
        return helper.ustr(self.obj)


class StStringHandler(StHandler):

    def escape(self, s):

        s = s.replace(u'\n', u'\\n')
        s = s.replace(u'\r', u'\\r')
        s = s.replace(u'\t', u'\\t')

        return s

    def handle(self):
        s = self.obj
        st = self.stype

        if st & C._ST_BYTES_:
            s = s.decode(S.encoding)

        s = helper.ustr(s)

        s = self.escape(s)

        str_encloser = helper.enclose_string(s, st)
        s = self.cut(s, str_encloser)
        str_encloser.body = s
                
        return helper.ustr(str_encloser)

    def cut(self, s, str_encloser):
        return s

class StStringHandlerLines(StStringHandler):
    """auto break long text into lines"""

    def cut(self, s, str_encloser):
        st = self.stype
        context = self.context

        left_margin = calc_string_left_margin(str_encloser, context)
        width = availiable_string_width(left_margin)

        if width > 0:
            seg_list = helper.wrap_string(
                str_encloser.body + 
                str_encloser.right_quotation_mark + 
                self.context.element_tail, 
                width)

            seg_list[-1] = seg_list[-1].rstrip(
                str_encloser.right_quotation_mark + 
                self.context.element_tail,
            )
            indent_char_width = helper.calc_width(S.leading)
            for i in range(1, len(seg_list)):
                seg_list[i] = ''.join([
                    left_margin//indent_char_width*S.leading,
                    left_margin%2*u' ',
                    seg_list[i],
                ])
            s = "\n".join(seg_list)

        return s


class StStringHandlerBriefly(StStringHandler):
    def cut(self, s, str_encloser):
        return string_cutter(s, str_encloser, self.context)


class StUndefinedHandlerBriefly(StUndefinedHandler):
    def handle(self):
        u = helper.ustr(self.obj)#.replace('\t', '\\t')
        return string_cutter(u, None, self.context)


def inline_msg(o, context):
    if isinstance(o, (int, float, tuple, list, dict, bytes, str, _unicode)):
        'base types'
        msg = typeval(o, context=context, type_editors={
            C._ST_BYTES_ | C._ST_UNICODE_ | C._ST_LITERAL_: StStringHandlerBriefly(),
            C._ST_UNDEFINED_: StUndefinedHandlerBriefly(),
        })
    else:
        'class definitions or class instances'
        msg = repr(o)

    return msg


def typeval(v, context=None, type_editors=None):
    if type_editors is None:

        type_editors = {
            C._ST_BYTES_ | C._ST_LITERAL_ | C._ST_UNICODE_: StStringHandler(),
            C._ST_UNDEFINED_: StUndefinedHandler(),
        }

    try:
        if S.united_str_coding_representation:
            st = string_type(v)
            ret = u''
            for stype, handler in type_editors.items():
                if stype & st:
                    ret = handler(v, st, context)
        else:
            ret = u'<YOU MUST SET S.united_str_coding_representation TO True>'

    except Exception as e:
        raise
        if S.priority_strategy == C._PS_CORRECTNESS_FIRST:
            print_exc_plus()
            raise e
        # S.priority_strategy == C._PS_CONTENT_FIRST:
        hx = v.decode("latin-1").encode("hex")
        ret = ustr("<CAN NOT PARSE OBJECT(hex:" + hx + "):" + str(e) + ">")

    return ret


def typeval_b(val, context):
    handler = None
    if S.text_wrap_enable:
        handler = StStringHandlerLines()
    else:
        handler = StStringHandler()
    type_editors = {
        C._ST_BYTES_ | C._ST_LITERAL_ | C._ST_UNICODE_: handler,
        C._ST_UNDEFINED_: StUndefinedHandler(),
    }
    return typeval(val, context, type_editors)


def string_type(s):
    if helper.pyv == 2:
        # in py2, string literal is both instance of str and bytes
        # a literal string is str (i.e: coding encoded, eg: utf8)
        # a u-prefixed string is unicode
        if isinstance(s, _unicode):
            return C._ST_UNICODE_
        elif isinstance(s, str):  # same as isinstance(v, bytes)
            return C._ST_LITERAL_ | C._ST_BYTES_
    else:
        # in py3, 
        # a literal string is str (i.e: unicode encoded)
        # a u-prefixed string is str
        # a utf8 string is bytes
        if isinstance(s, bytes):
            return C._ST_BYTES_
        elif isinstance(s, str):
            return C._ST_LITERAL_ | C._ST_UNICODE_

    return C._ST_UNDEFINED_


def too_long(leadCnt, position, obj):
    indent_str = leadCnt*S.leading

    choas = u''
    # assumpts its the value of list
    if position & C._AS_VALUE_:
        choas += '['
    choas += '\''

    terminal_x = get_terminal_size()[0]
    body = typeval(obj)
    whole_line_x = len(indent_str) + len(body)

    return terminal_x - whole_line_x <= 0


def calc_string_left_margin(str_encloser, context):
    left_margin = 0
    if context:
        left_filling = u''.join([
            context.leading,
            context.key_expr,
            context.sep_expr,
        ])
        left_margin = calc_width(left_filling)

    if str_encloser is not None:
        left_margin += calc_width(str_encloser.string_type_mark)
        left_margin += calc_width(str_encloser.left_quotation_mark)
    return left_margin


def availiable_string_width(left_margin):
    width = 0
    if S.text_wrap_method == C._TEXT_WRAP_BY_TERMINAL:
        width = get_terminal_size()[0] - left_margin
    elif S.text_wrap_method == C._TEXT_WRAP_BY_WIDTH:
        width = S.text_wrap_width - left_margin
    else:
        width = 0

    return width


def string_cutter(s, str_encloser, context):
    left_margin = calc_string_left_margin(str_encloser, context)
    width = availiable_string_width(left_margin)
    s_width = calc_width(s)
    msg = s
    if s_width > width:
        tail = context.element_tail if context else ''
        info = u'...(len=%d)' % (s_width)
        msg = cut_string(s, width - calc_width(info+tail))
        msg += info
    return msg
