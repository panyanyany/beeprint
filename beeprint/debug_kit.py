# -*- coding:utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from . import settings as S
from . import constants as C


### global variables
G_leading_char = '  '

def add_leading(depth, text):
    text = G_leading_char*depth + text
    text = text.replace('\n', '\n' + G_leading_char*depth)
    return text

def debug(level, depth, text):
    if S.debug is False:
        return
    text = add_leading(depth, text)
    print(text)
