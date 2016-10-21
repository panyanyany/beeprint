# -*- coding:utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division

import urwid
import unicodedata

from beeprint import constants as C
from beeprint import helper
from beeprint.utils import pyv, _unicode
from beeprint.terminal_size import get_terminal_size


def calc_width(s):
    return urwid.str_util.calc_width(s, 0, len(s))


def cut_string(s, length):
    assert length > 0, "length must be positive"

    t = urwid.Text(s)
    seg_list = t.render((length,)).text
    a_str = seg_list[0].rstrip().decode('utf8')
    if pyv == 2:
        # to unicode
        a_str = a_str.decode('utf8')
    return a_str


def too_long(indent_char, indent_cnt, position, inst_of_repr_block):
    indent_str = indent_cnt*indent_char

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


def get_line_width(method, width=None):
    _width = 0
    if method == C._STRING_BREAK_BY_TERMINAL:
        _width = get_terminal_size()[0]
    elif method == C._STRING_BREAK_BY_WIDTH:
        _width = width

    return _width


def shrink_string(s, width):
    """cut string, and show how many have been cut,
    the result length of string would not longer than width
    """

    s_width = calc_width(s)
    if s_width > width:
        info = u'...(len=%d)' % (s_width)
        length = width - calc_width(info)
        if length > 0:
            s = cut_string(s, length)
        elif length == 0:
            s = ''
        else:
            return (s, -1*length)

        s += info

    return (s, 0)


def shrink_inner_string(ctx, method, width=None, wrapper=None):
    s = ctx.obj
    left_margin = calc_left_margin(ctx, wrapper)
    right_margin = calc_right_margin(ctx, wrapper)

    # calculate availiable width for string
    a_width = get_line_width(method, width) - left_margin - right_margin

    if a_width <= 0:
        a_width = 1 # 1 just a random value to make it positive

    s, lack = shrink_string(s, a_width)
    if lack:
        s, lack = shrink_string(s, a_width + lack)

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


# copy from https://github.com/wolever/pprintpp
#
# pprintpp will make an attempt to print as many Unicode characters as is
# safely possible. It will use the character category along with this table to
# determine whether or not it is safe to print a character. In this context,
# "safety" is defined as "the character will appear visually distinct" -
# combining characters, spaces, and other things which could be visually
# ambiguous are repr'd, others will be printed. I made this table mostly by
# hand, mostly guessing, so please file bugs.
# Source: http://www.unicode.org/reports/tr44/#GC_Values_Table
unicode_printable_categories = {
    "Lu": 1, # Uppercase_Letter	an uppercase letter
    "Ll": 1, # Lowercase_Letter	a lowercase letter
    "Lt": 1, # Titlecase_Letter	a digraphic character, with first part uppercase
    "LC": 1, # Cased_Letter	Lu | Ll | Lt
    "Lm": 0, # Modifier_Letter	a modifier letter
    "Lo": 1, # Other_Letter	other letters, including syllables and ideographs
    "L":  1, # Letter	Lu | Ll | Lt | Lm | Lo
    "Mn": 0, # Nonspacing_Mark	a nonspacing combining mark (zero advance width)
    "Mc": 0, # Spacing_Mark	a spacing combining mark (positive advance width)
    "Me": 0, # Enclosing_Mark	an enclosing combining mark
    "M":  1, # Mark	Mn | Mc | Me
    "Nd": 1, # Decimal_Number	a decimal digit
    "Nl": 1, # Letter_Number	a letterlike numeric character
    "No": 1, # Other_Number	a numeric character of other type
    "N":  1, # Number	Nd | Nl | No
    "Pc": 1, # Connector_Punctuation	a connecting punctuation mark, like a tie
    "Pd": 1, # Dash_Punctuation	a dash or hyphen punctuation mark
    "Ps": 1, # Open_Punctuation	an opening punctuation mark (of a pair)
    "Pe": 1, # Close_Punctuation	a closing punctuation mark (of a pair)
    "Pi": 1, # Initial_Punctuation	an initial quotation mark
    "Pf": 1, # Final_Punctuation	a final quotation mark
    "Po": 1, # Other_Punctuation	a punctuation mark of other type
    "P":  1, # Punctuation	Pc | Pd | Ps | Pe | Pi | Pf | Po
    "Sm": 1, # Math_Symbol	a symbol of mathematical use
    "Sc": 1, # Currency_Symbol	a currency sign
    "Sk": 1, # Modifier_Symbol	a non-letterlike modifier symbol
    "So": 1, # Other_Symbol	a symbol of other type
    "S":  1, # Symbol	Sm | Sc | Sk | So
    "Zs": 0, # Space_Separator	a space character (of various non-zero widths)
    "Zl": 0, # Line_Separator	U+2028 LINE SEPARATOR only
    "Zp": 0, # Paragraph_Separator	U+2029 PARAGRAPH SEPARATOR only
    "Z":  1, # Separator	Zs | Zl | Zp
    "Cc": 0, # Control	a C0 or C1 control code
    "Cf": 0, # Format	a format control character
    "Cs": 0, # Surrogate	a surrogate code point
    "Co": 0, # Private_Use	a private-use character
    "Cn": 0, # Unassigned	a reserved unassigned code point or a noncharacter
    "C":  0, # Other	Cc | Cf | Cs | Co | Cn
}

def is_printable(char):
    return unicode_printable_categories.get(unicodedata.category(char))
