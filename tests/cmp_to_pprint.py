# -*- coding:utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import

from imp import reload

import unittest
import os
import sys
import types
import inspect
import codecs


CUR_SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
BEEPRINT_PATH = os.path.abspath(os.path.join(CUR_SCRIPT_PATH, '..'))
sys.path.append(BEEPRINT_PATH)

if sys.version_info < (3, 0):
    # avoid throw [UnicodeEncodeError: 'ascii' codec can't encode characters]
    # exceptions, without these lines, the sys.getdefaultencoding() returns ascii
    reload(sys)
    sys.setdefaultencoding('utf-8')

    pyv = 2
else:
    unicode = str
    pyv = 3

from beeprint import beeprint as pp, pyv
from beeprint import settings as S 
from beeprint import constants as C 
from pprint import pprint

try:
    from . import definition as df
except:
    import definition as df


def pair_print(title, v):
    print(title)
    print("----")
    print("**pprint:**\n```")
    pprint(v)
    print("```\n")
    print("**beeprint:**\n```")
    pp(v)
    print("```\n")


def main():
    if len(sys.argv) == 1:
        
        S.text_wrap_method = C._TEXT_WRAP_BY_WIDTH
        pair_print("Print dict", df.dict_multi_keys)
        pair_print("Print class", df.NormalClassNewStyle)
        pair_print("Print instance", df.inst_of_normal_class_new_style)
        pair_print("Print long text", df.long_text_in_list)
        return

    for i in range(1, len(sys.argv)):
        fn = sys.argv[i]
        args[fn]()

if __name__ == '__main__':
    main()
