# -*- coding:utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
import inspect
import sys
import types

from . import constants as C
from .helper import ustr, typeval


def pair_block_key(position, key):
    if position & C._AS_CLASS_ELEMENT_:
        # class method name or attribute name no need to add u or b prefix
        key = ustr(key)
    else:
        key = typeval(key)

    return key
