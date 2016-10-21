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
import re


CUR_SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
BEEPRINT_PATH = os.path.abspath(os.path.join(CUR_SCRIPT_PATH, '..'))
sys.path.insert(0, BEEPRINT_PATH)

if sys.version_info < (3, 0):
    # avoid throw [UnicodeEncodeError: 'ascii' codec can't encode characters]
    # exceptions, without these lines, the sys.getdefaultencoding() returns ascii
    reload(sys)
    sys.setdefaultencoding('utf-8')

    pyv = 2
else:
    unicode = str
    pyv = 3

from pprintpp import pprint as ppp
from beeprint import pp, pyv, Config
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

def has_custom_repr(o):
    repr_typ_name = lambda o: type(o.__repr__).__name__
    builtin_repr_names = ['method-wrapper', 'wrapper_descriptor', 'method-wrapper']
    return hasattr(o, '__repr__') and repr_typ_name(o) not in builtin_repr_names


def get_decorators(o):
    sourcelines = inspect.getsourcelines(o)[0]
    decorators = []
    for line in sourcelines:
        line = line.strip()
        if line.startswith('@'):
            match = re.search('@(.*)[\(]*', line)
            if not match:
                print('unmatch line', line)
                continue
            decorators.append(match.group(1))

    return decorators


def test_class_repr():
    reprs = [
        df.ReprMethodClassOldStyle,
        df.ReprMethodClassNewStyle,
        df.ReprStaticClassOldStyle,
        df.ReprStaticClassNewStyle,
        df.ReprClassMethodClassOldStyle,
        df.ReprClassMethodClassNewStyle,
        df.ReprLambdaClassOldStyle,
        df.ReprLambdaClassNewStyle,
    ]
    values = [
        df.EmptyFunc,
        df.EmptyClassOldStyle,
        df.EmptyClassNewStyle,
        df.NormalClassOldStyle,
        df.NormalClassNewStyle,
        df.inst_of_normal_class_old_style,
        df.inst_of_normal_class_new_style,
        df.ReprMethodClassNewStyle,
    ]
    typ = lambda e: type(e.__repr__).__name__
    for c in values+reprs:
        print('%60s %s' % (c, has_custom_repr(c)))

    print()
    for c in reprs:
        # print('%60s %20s %20s' % (c, typ(c), typ(c())))
        print('%60s %s:%20s %s:%20s' % (c, get_decorators(c.__repr__), typ(c), get_decorators(c().__repr__), typ(c())))
        # print('%60s %20s %-20s' % (c, typ(c), repr(c())))


def main():
    if len(sys.argv) == 1:
        # S.debug_level = 9
        # S.str_display_not_prefix_u = False
        # S.str_display_not_prefix_b = False

        # S.max_depth = 1
        tweet = {'coordinates': None, 'created_at': 'Mon Jun 27 19:32:19 +0000 2011', 'entities': {'hashtags': [], 'urls': [{'display_url': 'tumblr.com/xnr37hf0yz', 'expanded_url': 'http://tumblr.com/xnr37hf0yz', 'indices': [107, 126], 'url': 'http://t.co/cCIWIwg'}], 'user_mentions': []}, 'place': None, 'source': '<a href="http://www.tumblr.com/" rel="nofollow">Tumblr</a>', 'truncated': False, 'user': {'contributors_enabled': True, 'default_profile': False, 'entities': {'hashtags': [], 'urls': [], 'user_mentions': []}, 'favourites_count': 20, 'id_str': '6253282', 'profile_link_color': '0094C2'}}
        tweet = {'entities': {'hashtags': [], 'urls': [{'display_url': 'tumblr.com/xnr37hf0yz', 'expanded_url': 'http://tumblr.com/xnr37hf0yz', 'indices': [107, 126], 'url': 'http://t.co/cCIWIwg'}], 'user_mentions': []}}
        # pp(tweet)
        # df.test_boundary_break()
        # df.test_complicate_data()
        df.test_inline_repr_out_of_range()
        # config = Config()
        # config.max_depth = 3
        # config.debug_level = 9
        # pp(sys.modules['inspect'].Parameter.KEYWORD_ONLY, config=config)
        # pp(sys.modules['re']._cache)
        # pp(sys.modules, config=config)
        # df.test_class_last_el()
        # df.test_inner_class()
        # df.test_autoclip_no_room()
        # df.test_class_all_repr_disable()
        # df.test_class_inst_repr_enable()

        # import pygments.unistring
        # pp(sys.modules['pygments.unistring'].Cs)
        # ppp(sys.modules['pygments.unistring'].Cs)
        # print(sys.modules['pygments.unistring'].Cs)

        # df.test_sort_of_string()
        # ppp(df.sort_of_string)
        # df.test_recursion()
        # df.test_tuple_nested()

        return

    for i in range(1, len(sys.argv)):
        fn = sys.argv[i]
        args[fn]()

if __name__ == '__main__':
    main()
