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

from . import settings as S
from . import constants as C
from .utils import print_exc_plus
from .models.block import Block


def beeprint(o, output=True):
    """print data beautifully

    >>> beeprint(1)
    1

    >>> beeprint(1.1)
    1.1

    >>> beeprint(-1)
    -1

    >>> beeprint(-1.1)
    -1.1

    >>> beeprint("plain string")
    'plain string'

    >>> beeprint(u'unicode string')
    'unicode string'

    >>> beeprint(u'utf8 string'.encode('utf-8'))
    'utf8 string'

    >>> beeprint(u'gb2312 string'.encode('gb2312'))
    'gb2312 string'

    >>> beeprint(u'\\\\')
    '\\'

    >>> beeprint(u'\\\\'.encode("utf8"))
    '\\'
    """
    res = str(Block(o))
    if output and not S.write_to_buffer_when_execute:
        try:
            print(res, end='')
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
