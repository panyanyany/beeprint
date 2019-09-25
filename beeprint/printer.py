# -*- coding:utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
import sys
import traceback
import types
import inspect

from io import StringIO

from .utils import pyv

if pyv == 2:
    # avoid throw [UnicodeEncodeError: 'ascii' codec can't encode characters]
    # exceptions, without these lines, the sys.getdefaultencoding() returns ascii
    from imp import reload

    reload(sys)
    sys.setdefaultencoding('utf-8')

from . import constants as C
from .utils import print_exc_plus
from .models.block import Block, Context
from .config import Config
from .debug_kit import print_obj_path


def pp(o, output=True, max_depth=5, indent=2, width=80, sort_keys=True, string_break_enable=True,
       hide_attr_by_prefixes=Config.prop_leading_filters,
       config=None,
       **kwargs):
    """print data beautifully
    """

    if config:
        config = config.clone()
    else:
        config = Config()

        assert max_depth > 0
        config.max_depth = max_depth

        assert indent > 0
        config.indent_char = u' ' * indent

        assert width >= 0
        config.string_break_width = width

        config.prop_leading_filters = hide_attr_by_prefixes

        if string_break_enable is False:
            config.string_break_enable = False
            config.string_break_method = C._STRING_BREAK_BY_NONE

        config.dict_ordered_key_enable = bool(sort_keys)
        for k, v in kwargs.items():
            if getattr(config, k):
                setattr(config, k, v)

    if not output:
        config.stream = None

    try:
        res = str(Block(config, Context(obj=o)))
    except:
        try:
            print_obj_path()
        except:
            pass
        raise
    if config.debug_level != 0:
        if config.debug_delay:
            print(config.debug_stream.getvalue())

    if not output:
        return res
