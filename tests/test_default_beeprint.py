# -*- coding:utf-8 -*-

import unittest
import os
import sys

CUR_SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
BEEPRINT_PATH = os.path.abspath(os.path.join(CUR_SCRIPT_PATH, '..'))
sys.path.append(BEEPRINT_PATH)

from beeprint.printer import beeprint, pyv
from beeprint import settings as S


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

class TestSimpleTypes(unittest.TestCase):

    def setUp(self):
        pass

    def test_positive(self):
        self.assertEqual(beeprint(1, output=False), '1\n')
        self.assertEqual(beeprint(1.1, output=False), '1.1\n')

    def test_negative(self):
        self.assertEqual(beeprint(-1, output=False), '-1\n')
        self.assertEqual(beeprint(-1.1, output=False), '-1.1\n')

    def test_string(self):
        # string literal
        # S.debug = True
        S.str_display_not_prefix_u = False
        S.str_display_not_prefix_b = False
        if pyv == 2:
            self.assertEqual(beeprint("plain string", output=False), "b'plain string'\n")
        elif pyv == 3:
            self.assertEqual(beeprint("plain string", output=False), "u'plain string'\n")

        # unicode string
        s = u'unicode string'
        self.assertEqual(beeprint(s, output=False), u"u'unicode string'\n")

        # utf8 string
        s = u'utf8 string'.encode('utf-8')
        self.assertEqual(beeprint(s, output=False), u"b'utf8 string'\n")

        # gb2312 string
        s = u'gb2312 string'.encode('gb2312')
        self.assertEqual(beeprint(s, output=False), u"b'gb2312 string'\n")

        # unicode special characters string
        s = u'\\'
        self.assertEqual(beeprint(s, output=False), u"u'\\'\n")

        # utf8 special characters string
        s = u'\\'.encode("utf8")
        self.assertEqual(beeprint(s, output=False), u"b'\\'\n")

    def test_complicate_data(self):
        S.str_display_not_prefix_u = False
        S.str_display_not_prefix_b = False

        ans = u""
        with open(os.path.join(CUR_SCRIPT_PATH, 
                               'data/tests_complicate_data.txt')) as fp:
            ans = fp.read()

        # to prevent comparing fail in unordered keys to dict
        ans2 = u""
        with open(os.path.join(CUR_SCRIPT_PATH, 
                               'data/tests_complicate_data2.txt')) as fp:
            ans2 = fp.read()

        res = beeprint(values, output=False)
        self.assertEqual(res == ans or res == ans2, True)


if __name__ == '__main__':
    unittest.main()
