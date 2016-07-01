# -*- coding:utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division

from . import utils
from . import settings as S

import urwid


class Linizer(object):
    """ make a line of string to print """

    left_quoter = "'"
    right_quoter = "'"

    seperator = ":"
    after_seperator = " "

    def __init__(self, position=None, lead_cnt=None, key=None, value=None):

        self.position = position
        self.lead_cnt = lead_cnt
        self.key = key
        self.value = value

        self.value_left_brace = None
        self.value_right_brace = None

    def __str__(self):
        joint = [
            S.leading * self.lead_cnt,
        ]
        if self.key is not None:
            joint += [
                # self.left_quoter,
                self.key,
                # self.right_quoter,

                self.seperator,
            ]

            if self.value is not None:
                joint += [
                    self.after_seperator,
                ]

        # value left brace
        if self.value_left_brace is not None:
            joint += [self.value_left_brace]

        # value
        if self.value is not None:
            joint += [self.value]

        # value right brace
        if self.value_right_brace is not None:
            joint += [self.value_right_brace]

        # tail
        if self.value is not None:
            joint += [self.tail]

        # new line
        joint += [
            '\n',
        ]

        return ''.join(joint)

    @property
    def tail(self):
        return utils.tail_symbol(self.position)


class Context(object):

    left_quoter = "'"
    right_quoter = "'"

    seperator = ":"
    after_seperator = " "

    def __init__(self, indent_char=None, position=None, lead_cnt=None, key=None, value=None):

        self.indent_char = indent_char
        self.position = position
        self.lead_cnt = lead_cnt
        self.key = key
        self.value = value

        self.value_left_brace = None
        self.value_right_brace = None

    @property
    def leading(self):
        return self.indent_char*self.lead_cnt

    @property
    def key_expr(self):
        if self.key is None:
            return ''
        from .block_helper import pair_block_key
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

class Block(object):
    parent = None
    position = None
    indent_cnt = None
    subject = None
