# -*- coding:utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from . import settings as S
from . import constants as C
import inspect


### global variables
G_leading_char = '  '

def add_leading(depth, text):
    text = G_leading_char*depth + text
    text = text.replace('\n', '\n' + G_leading_char*depth)
    return text

def debug(level, depth, text):
    if S.debug_level >= level:
        frame_list = inspect.stack()
        frame_obj = frame_list[1][0]
        class_name = frame_obj.f_locals['self'].__class__.__name__
        caller_name = frame_list[1][3]
        depth = len(frame_list) - 4
        if level == C._DL_FUNC_:
            depth -= 1
            text = class_name + '.' + caller_name + ': ' + text
        text = add_leading(depth, text)
        print(text)
