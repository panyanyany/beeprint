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
        self.assertEqual(beeprint("plain string", output=False), '"plain string"\n')

        # unicode string
        s = u'unicode string'
        if pyv == 2:
            self.assertEqual(beeprint(s, output=False), u"u'unicode string'\n")
        elif pyv == 3:
            self.assertEqual(beeprint(s, output=False), u'"unicode string"\n')

        # utf8 string
        s = u'utf8 string'.encode('utf-8')
        if pyv == 2:
            self.assertEqual(beeprint(s, output=False), "\"utf8 string\"\n")
        elif pyv == 3:
            self.assertEqual(beeprint(s, output=False), "b'utf8 string'\n")


if __name__ == '__main__':
    unittest.main()
