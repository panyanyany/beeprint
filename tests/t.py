# -*- coding:utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import

from imp import reload

import unittest
import os
import sys
import types
import inspect


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

from beeprint.printer import beeprint as pp, pyv
from beeprint import settings as S 
from beeprint import constants as C 

try:
    from .definition import values
    from .definition import inst_of_normal_class_old_style, inst_of_normal_class_new_style, NormalClassOldStyle, NormalClassNewStyle, EmptyFunc
    from . import definition as df
except:
    from definition import values
    from definition import inst_of_normal_class_old_style, inst_of_normal_class_new_style, NormalClassOldStyle, NormalClassNewStyle, EmptyFunc
    import definition as df


# >> utilities
def detect_same_attrs(*args):
    d_attrs_by_val_list = {} 
    for e in args:
        for attr in dir(e):
            d_attrs_by_val_list.setdefault(attr, [])
            d_attrs_by_val_list[attr].append(e)

    same_attrs = []
    for attr, values in d_attrs_by_val_list.items():
        if len(values) == len(args):
            same_attrs.append((attr, values))

    same_attrs.sort(key=lambda e: e[0])

    return same_attrs
# << utilities

def class_test():
    pass

def inst_test():
    for v in values:
        try:
            print('%40s: %s' % (v, v.__module__))
        except:
            pass
        continue
        if pyv == 2:
            print('%40s: %s' % (v, isinstance(v, (types.InstanceType, object))))
        else:
            print('%40s: %s' % (v, isinstance(v, object)))

    same_attrs = detect_same_attrs(inst_of_normal_class_old_style, inst_of_normal_class_new_style)
    for attr, v in same_attrs:
        print('%40s: %s' % (attr, v))

def builtin_test():
    for v in [EmptyFunc, NormalClassOldStyle.mth, NormalClassNewStyle.mth, inst_of_normal_class_old_style.mth, inst_of_normal_class_new_style.mth]:
        # print('%40s: %s' % (v, isinstance(v, types.MethodType))) py2 all true
        # print('%40s: %s' % (v, inspect.ismethod(v))) py2 all true
        # print('%40s: %s' % (v, inspect.isbuiltin(v))) py2 all false
        # print('%40s: %s' % (v, inspect.ismethod(v))) py3 FFTT
        print('%40s: %s, %s' % (v, v.__qualname__, inspect.getargspec(v).args))


args = {
    "class_test": class_test,
    "inst_test": inst_test,
    "builtin_test": builtin_test,
}

def main():
    if len(sys.argv) == 1:
        # S.debug_level = 9
        # S.str_display_not_prefix_u = False
        # S.str_display_not_prefix_b = False

        # S.max_depth = 3
        S.text_wrap_method = C._TEXT_WRAP_BY_WIDTH
        pp(df.values)
        pp(df.long_text_in_dict)
        pp(df.long_text_in_list)
        return

    for i in range(1, len(sys.argv)):
        fn = sys.argv[i]
        args[fn]()

if __name__ == '__main__':
    main()
