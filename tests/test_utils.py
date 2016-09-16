# -*- coding:utf-8 -*-

import unittest
import os
import sys
import codecs

CUR_SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
BEEPRINT_PATH = os.path.abspath(os.path.join(CUR_SCRIPT_PATH, '..'))
sys.path.append(BEEPRINT_PATH)

from beeprint import pp, pyv
from beeprint.utils import is_class_instance

import definition as df

class TestUtils(unittest.TestCase):

    def setUp(self):
        pass

    def test_is_class_instance(self):
        self.assertEqual(is_class_instance(None), False)
        self.assertEqual(is_class_instance(1), False)
        self.assertEqual(is_class_instance((1,)), False)
        self.assertEqual(is_class_instance([]), False)
        self.assertEqual(is_class_instance({}), False)
        self.assertEqual(is_class_instance(tuple), False)
        self.assertEqual(is_class_instance(list), False)
        self.assertEqual(is_class_instance(dict), False)
        self.assertEqual(is_class_instance(df.EmptyFunc), False)
        self.assertEqual(is_class_instance(df.EmptyClassOldStyle), False)
        self.assertEqual(is_class_instance(df.EmptyClassNewStyle), False)
        self.assertEqual(is_class_instance(df.NormalClassOldStyle.mth), False)
        self.assertEqual(is_class_instance(df.NormalClassOldStyle.mth), False)

        self.assertEqual(is_class_instance(df.EmptyClassOldStyle()), True)
        self.assertEqual(is_class_instance(df.EmptyClassNewStyle()), True)
        self.assertEqual(is_class_instance(df.NormalClassOldStyle().mth), False)
        self.assertEqual(is_class_instance(df.NormalClassOldStyle().mth), False)

if __name__ == '__main__':
    unittest.main()
