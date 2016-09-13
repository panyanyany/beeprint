# -*- coding:utf-8 -*-

import unittest
import os
import sys
import codecs

CUR_SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
BEEPRINT_PATH = os.path.abspath(os.path.join(CUR_SCRIPT_PATH, '..'))
sys.path.append(BEEPRINT_PATH)

from beeprint.printer import beeprint, pyv
from beeprint import settings as S
from beeprint import helper


class TestHelper(unittest.TestCase):

    def setUp(self):
        pass

    def test_class_method(self):
        self.assertEqual(helper.inline_msg(1), '1')
        self.assertEqual(helper.inline_msg('aaaaaaaaaaaaaaaaaaaaaaaaaaaa'*10),
                         'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa...(len=280)')
        self.assertEqual(helper.inline_msg(os)[:18],
                         "<module 'os' from ");


if __name__ == '__main__':
    unittest.main()
