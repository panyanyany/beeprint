# -*- coding:utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division

import urwid

from beeprint import constants as C
from beeprint import settings as S
from beeprint import helper
from beeprint.utils import pyv, _unicode
from beeprint.terminal_size import get_terminal_size


def calc_width(s):
    return urwid.str_util.calc_width(s, 0, len(s))


def cut_string(s, length):
    t = urwid.Text(s)
    seg_list = t.render((length,)).text
    a_str = seg_list[0].rstrip().decode('utf8')
    if pyv == 2:
        # to unicode
        a_str = a_str.decode('utf8')
    return a_str


def too_long(leadCnt, position, inst_of_repr_block):
    indent_str = leadCnt*S.indent_char

    choas = u''
    # assumpts its the value of list
    if position & C._AS_VALUE_:
        choas += '['
    choas += '\''

    terminal_x = get_terminal_size()[0]
    body = str(inst_of_repr_block)
    whole_line_x = len(indent_str) + len(body)

    return terminal_x - whole_line_x <= 0


def calc_left_margin(ctx, wrapper=None):
    left_filling = u''.join([
        ctx.indent,
        ctx.key_expr,
        ctx.sep_expr,
    ])
    left_margin = calc_width(left_filling)

    if wrapper is not None:
        left_margin += calc_width(wrapper.get_prefix())

    return left_margin


def calc_right_margin(ctx, wrapper=None):
    right_chars = ''
    if wrapper:
        right_chars += wrapper.get_suffix()

    right_chars += ctx.element_ending

    return calc_width(right_chars)


def get_line_width():
    width = 0
    if S.string_break_method == C._STRING_BREAK_BY_TERMINAL:
        width = get_terminal_size()[0]
    elif S.string_break_method == C._STRING_BREAK_BY_WIDTH:
        width = S.string_break_width

    return width


def shrink_string(s, width):
    """cut string, and show how many have been cut,
    the result length of string would not longer than width
    """

    s_width = calc_width(s)
    if s_width > width:
        info = u'...(len=%d)' % (s_width)
        s = cut_string(s, width - calc_width(tail))
        s += info

    return s


def shrink_inner_string(ctx, wrapper=None):
    s = ctx.obj
    left_margin = calc_left_margin(ctx, wrapper)
    right_margin = calc_right_margin(ctx, wrapper)

    # calculate availiable width for string
    a_width = get_line_width() - left_margin - right_margin

    s_width = calc_width(s)
    if s_width > a_width:
        info = u'...(len=%d)' % (s_width)
        s = cut_string(s, a_width - calc_width(info))
        s += info

    ctx.obj = s
    return s


def break_string(s, width):
    """break string into segments but would not break word
    works well with Chinese, English
    """

    t = urwid.Text(s)
    seg_list = t.render((width,)).text
    seg_list = [seg.rstrip() for seg in seg_list]
    if pyv == 3:
        # seg is the type of <class 'bytes'> in py3
        # seg is the type of <type 'str'> in py2
        seg_list = [seg.decode('utf8') for seg in seg_list]
    return seg_list
