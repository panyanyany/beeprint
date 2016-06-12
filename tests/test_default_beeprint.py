# -*- coding:utf-8 -*-

import unittest
import os
import sys

CUR_SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
BEEPRINT_PATH = os.path.abspath(os.path.join(CUR_SCRIPT_PATH, '..'))
sys.path.append(BEEPRINT_PATH)

from beeprint.printer import beeprint, pyv
from beeprint import settings as S


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


if __name__ == '__main__':
    unittest.main()
