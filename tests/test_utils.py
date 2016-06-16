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
from beeprint.utils import is_class_method, is_instance_method

try:
    from .definition import values, c, c2, ic, ic2, f
except:
    from definition import values, c, c2, ic, ic2, f

class TestUtils(unittest.TestCase):

    def setUp(self):
        pass

    def test_class_method(self):
        self.assertEqual(is_class_method('', f), False)
        self.assertEqual(is_class_method('', c.mth), True)
        self.assertEqual(is_class_method('', c2.mth), True)
        self.assertEqual(is_class_method('', ic.mth), False)
        self.assertEqual(is_class_method('', ic2.mth), False)

    def test_instance_method(self):
        self.assertEqual(is_instance_method('', f), False)
        self.assertEqual(is_instance_method('', c.mth), False)
        self.assertEqual(is_instance_method('', c2.mth), False)
        self.assertEqual(is_instance_method('', ic.mth), True)
        self.assertEqual(is_instance_method('', ic2.mth), True)


if __name__ == '__main__':
    unittest.main()
