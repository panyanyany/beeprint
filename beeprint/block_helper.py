# -*- coding:utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
import inspect
import sys
import types

from . import constants as C
from .helper import pstr, typeval


def pair_block_key(position, key):
    if position & C._AS_CLASS_ELEMENT_:
        # class method name or attribute name no need to add u or b prefix
        key = pstr(key)
    else:
        key = typeval(None, key)

    return key
