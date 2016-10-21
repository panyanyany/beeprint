# -*- coding:utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
import sys
import types

from io import StringIO
from . import constants as C
from . import utils



class Config(object):

    def clone(self):
        obj = Config()
        for k,v in self.__dict__.items():
            setattr(obj, k, v)
        return obj

    # >> coding
    encoding = 'utf-8'

    # >> representation
    max_depth = 5
    indent_char = u'  '
    newline = False
    tuple_in_line = True
    list_in_line = True

    # >> stream
    stream = sys.stdout

    # >> class control

    # filter out attributes by prefix
    prop_leading_filters = ["__", "func_"]
    # filter out attributes by name or judgement function
    prop_filters = [utils.is_pan_function, 'im_func', 'im_self', 'im_class']

    # call user-defined __repr__() on class
    # class_repr_enable = False

    # call user-defined __repr__() on class instance
    instance_repr_enable = True

    # >> 优先策略
    # to raise exception or not when errors happened
    # _PS_CONTENT_FIRST will keep content printing despite of any error
    priority_strategy = C._PS_CONTENT_FIRST

    # debug = False
    debug_level = 0
    debug_stream = StringIO()
    # print info after pp()
    debug_delay = True

    # >> string control
    # united_str_coding_representation
    # In spite of python version
    # unicode string will be displayed as u''
    # non-unicode string will be displayed as b''
    united_str_coding_representation = True
    str_display_lqm = '\''
    str_display_rqm = '\''
    str_display_not_prefix_u = True
    str_display_not_prefix_b = True
    str_display_escape_special_char = True

    element_display_last_with_comma = True

    # >> long string control
    string_break_enable = True
    string_break_method = C._STRING_BREAK_BY_TERMINAL
    string_break_width = 80

    # >> auto clip text
    text_autoclip_enable = True
    text_autoclip_method = C._TEXT_AUTOCLIP_BY_LINE
    # enabled if text_autoclip_method is _TEXT_AUTOCLIP_BY_LINE
    # and string_break_enable is True
    text_autoclip_maxline = 2
    # enabled if text_autoclip_method is _TEXT_AUTOCLIP_BY_LENGTH
    # text_autoclip_maxlength = 80

    # >> dict
    # print dict with ordered keys
    dict_ordered_key_enable = True

    # >> output control
    output_briefly_enable = True
    output_briefly_method = C._OB_BY_LEVEL
