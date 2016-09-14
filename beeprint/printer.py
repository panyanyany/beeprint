# -*- coding:utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
import sys
import traceback
import types
import inspect

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


def pp(o, output=True, max_depth=None, config=None):
    """print data beautifully
    """

    config = config or Config()
    if max_depth:
        config.max_depth = max_depth

    res = str(Block(config, Context(obj=o)))
    if output and not config.write_to_buffer_when_execute:
        try:
            print(res, end='')
            # return res
        except Exception as e:
            print_exc_plus()
            if type(e) is UnicodeEncodeError:
                # UnicodeEncodeError: 'ascii' codec can't encode characters in
                # position 35-36: ordinal not in range(128)
                print(sys.getdefaultencoding())
                print('res value type:', type(res))
            else:
                print('exception type :', type(e))
    else:
        return res
