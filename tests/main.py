# -*- coding:utf-8 -*-

import unittest
import os
import sys
import codecs
import re

CUR_SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
BEEPRINT_PATH = os.path.abspath(os.path.join(CUR_SCRIPT_PATH, '..'))
sys.path.append(BEEPRINT_PATH)

from beeprint import pyv
from beeprint import beeprint
from beeprint import settings as S
from beeprint import constants as C

try:
    from .definition import values
    import definition as df
except:
    from definition import values
    import definition as df


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
        # S.str_display_not_prefix_u = False
        # S.str_display_not_prefix_b = False
        S.text_wrap_method = C._TEXT_WRAP_BY_WIDTH
        S.text_autoclip_enable = False

        ans = u""
        data_path = os.path.join(CUR_SCRIPT_PATH, 
                                 'data/all_in_one.txt')
        with codecs.open(data_path, encoding="utf8") as fp:
            ans = fp.read()

        res = beeprint(values, output=False)
        res += beeprint(df.long_text_in_dict, output=False)
        res += beeprint(df.long_text_in_list, output=False)
        self.assertEqual(res, ans)
        # self.assertEqual(res, ans)

    def test_out_of_range(self):
        S.max_depth = 1

        ans = ""
        rel_path = ''
        if pyv == 2:
            rel_path = 'data/out_of_range_py2.txt'
        else:
            rel_path = 'data/out_of_range_py3.txt'
        data_path = os.path.join(CUR_SCRIPT_PATH, rel_path)
        with codecs.open(data_path, encoding='utf8') as fp:
            ans = fp.read()
        # delete object id, such as
        # <definition.NormalClassOldStyle object at 0x7f2d9a61bac8>
        ans, _ = re.subn("at 0x[\d\w]+", "", ans)

        res = beeprint(df.out_of_range, output=False)
        # delete object id, such as
        # <definition.NormalClassOldStyle object at 0x7f2d9a61bac8>
        res, _ = re.subn("at 0x[\d\w]+", "", res)
        
        self.assertEqual(res, ans)

    def test_out_of_range_in_dict(self):
        S.max_depth = 1

        ans = ""
        rel_path = 'data/out_of_range_in_dict.txt'
        data_path = os.path.join(CUR_SCRIPT_PATH, rel_path)
        with codecs.open(data_path, encoding='utf8') as fp:
            ans = fp.read()
        # delete object id, such as
        # <definition.NormalClassOldStyle object at 0x7f2d9a61bac8>
        ans, _ = re.subn("at 0x[\d\w]+", "", ans)

        res = beeprint(df.out_of_range_in_dict, output=False)
        # delete object id, such as
        # <definition.NormalClassOldStyle object at 0x7f2d9a61bac8>
        res, _ = re.subn("at 0x[\d\w]+", "", res)
        
        self.assertEqual(res, ans)


    def test_long_text(self):
        pass
        # res = beeprint(long_text_en, output=False)
        # self.assertEqual(res, ans)


class TestLineBreak(unittest.TestCase):
    
    def setUp(self):
        pass

    def test_boundary_break(self):
        rel_path = 'data/line_break/boundary_break.txt'
        data_path = os.path.join(CUR_SCRIPT_PATH, rel_path)
        with codecs.open(data_path, encoding='utf8') as fp:
            ans = fp.read()

        res = df.f_line_break_boundary(False)

        self.assertEqual(ans, res)


class TestAutoClip(unittest.TestCase):

    def setUp(self):
        pass

    def test_3lines_clip(self):
        rel_path = 'data/auto_clip/by_lines.txt'
        data_path = os.path.join(CUR_SCRIPT_PATH, rel_path)
        with codecs.open(data_path, encoding='utf8') as fp:
            ans = fp.read()

        res = df.test_3lines_clip(False)

        self.assertEqual(ans, res)


class TestDict(unittest.TestCase):

    def setUp(self):
        pass

    def test_ordered_keys(self):
        rel_path = 'data/dict/foo.txt'
        data_path = os.path.join(CUR_SCRIPT_PATH, rel_path)
        with codecs.open(data_path, encoding='utf8') as fp:
            ans = fp.read()

        res = df.test_dict_ordered_keys(False)

        self.assertEqual(ans, res)


if __name__ == '__main__':
    unittest.main()
