# -*- coding:utf-8 -*-
from __future__ import print_function

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
    from imp import reload
    reload(sys)
    sys.setdefaultencoding('utf-8')

    pyv = 2
else:
    unicode = str
    pyv = 3

from beeprint.printer import beeprint as pp, pyv
from beeprint import settings as S 

d = {
    "key": "val",
    "list": [1, 2, 3, "string", 1.2],
    "dict": {
        "key": "val",
    },
}

def f(): pass

class CE: pass
class CE2(object): pass

class c: 
    def mth():pass
    static_props = 1

class c2(object): 
    def mth():pass
    static_props = 1

ic = c()
ic2 = c2()

values = [
    1,
    1.1,
    "s",
    u"us",
    "a中文",
    u"a中文",
    [1],
    (1,2),
    f,
    CE,
    CE2,
    c,
    c2,
    ic,
    ic2,
    ic.mth,
    ic2.mth,
    {
        'key': 'val',
        u'key2': u'val',
    },
]

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

    same_attrs = detect_same_attrs(ic, ic2)
    for attr, v in same_attrs:
        print('%40s: %s' % (attr, v))

def builtin_test():
    for v in [ic.mth.im_func, ic2.mth.im_func]:
        print('%40s: %s' % (v, inspect.ismethod(v)))

args = {
    "class_test": class_test,
    "inst_test": inst_test,
    "builtin_test": builtin_test,
}

def main():
    if len(sys.argv) == 1:
        # S.debug_level = 9
        pp(values)
        # pp([ic.mth, ic2.mth])
        return

    for i in range(1, len(sys.argv)):
        fn = sys.argv[i]
        args[fn]()

if __name__ == '__main__':
    main()
