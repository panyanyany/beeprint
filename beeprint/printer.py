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


def pp(o, output=True, max_depth=None, config=None):
    """print data beautifully
    """

    config = (config and config.clone()) or Config()
    if max_depth:
        config.max_depth = max_depth

    if not output:
        config.stream = None

    try:
        res = str(Block(config, Context(obj=o)))
    except:
        print_obj_path()
        raise
    if config.debug_level != 0:
        if config.debug_delay:
            print(config.debug_stream.getvalue())

    if not output:
        return res
