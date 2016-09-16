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
from beeprint import pp
from beeprint import Config
from beeprint import constants as C

try:
    from .definition import values
    import definition as df
except:
    from definition import values
    import definition as df


class TestBase(unittest.TestCase):

    def setUp(self):
        pass


class TestSimpleTypes(TestBase):

    def test_positive(self):
        self.assertEqual(pp(1, output=False), '1\n')
        self.assertEqual(pp(1.1, output=False), '1.1\n')

    def test_negative(self):
        self.assertEqual(pp(-1, output=False), '-1\n')
        self.assertEqual(pp(-1.1, output=False), '-1.1\n')

    def test_string(self):
        # string literal
        config = Config()
        config.str_display_not_prefix_u = False
        config.str_display_not_prefix_b = False
        if pyv == 2:
            self.assertEqual(pp("plain string", output=False, config=config), "b'plain string'\n")
        elif pyv == 3:
            self.assertEqual(pp("plain string", output=False, config=config), "u'plain string'\n")

        # unicode string
        s = u'unicode string'
        self.assertEqual(pp(s, output=False, config=config), u"u'unicode string'\n")

        # utf8 string
        s = u'utf8 string'.encode('utf-8')
        self.assertEqual(pp(s, output=False, config=config), u"b'utf8 string'\n")

        # gb2312 string
        s = u'gb2312 string'.encode('gb2312')
        self.assertEqual(pp(s, output=False, config=config), u"b'gb2312 string'\n")

        # unicode special characters string
        s = u'\\'
        self.assertEqual(pp(s, output=False, config=config), u"u'\\\\'\n")

        # utf8 special characters string
        s = u'\\'.encode("utf8")
        self.assertEqual(pp(s, output=False, config=config), u"b'\\\\'\n")

    def test_complicate_data(self):
        config = Config()
        config.string_break_method = C._STRING_BREAK_BY_WIDTH
        config.text_autoclip_enable = False

        ans = u""
        data_path = os.path.join(CUR_SCRIPT_PATH, 
                                 'data/all_in_one.txt')
        with codecs.open(data_path, encoding="utf8") as fp:
            ans = fp.read()

        res = pp(values, output=False, config=config)
        res += pp(df.long_text_in_dict, output=False, config=config)
        res += pp(df.long_text_in_list, output=False, config=config)
        self.assertEqual(res, ans)
        # self.assertEqual(res, ans)

    def test_out_of_range(self):
        config = Config()
        config.max_depth = 1

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

        res = pp(df.out_of_range, output=False, config=config)
        # delete object id, such as
        # <definition.NormalClassOldStyle object at 0x7f2d9a61bac8>
        res, _ = re.subn("at 0x[\d\w]+", "", res)
        
        self.assertEqual(res, ans)

    def test_out_of_range_in_dict(self):
        config = Config()
        config.max_depth = 1

        ans = ""
        rel_path = 'data/out_of_range_in_dict.txt'
        data_path = os.path.join(CUR_SCRIPT_PATH, rel_path)
        with codecs.open(data_path, encoding='utf8') as fp:
            ans = fp.read()
        # delete object id, such as
        # <definition.NormalClassOldStyle object at 0x7f2d9a61bac8>
        ans, _ = re.subn("at 0x[\d\w]+", "", ans)

        res = pp(df.out_of_range_in_dict, output=False, config=config)
        # delete object id, such as
        # <definition.NormalClassOldStyle object at 0x7f2d9a61bac8>
        res, _ = re.subn("at 0x[\d\w]+", "", res)
        
        self.assertEqual(res, ans)


    def test_long_text(self):
        pass
        # res = pp(long_text_en, output=False, config=config)
        # self.assertEqual(res, ans)


class TestLineBreak(TestBase):
    
    def test_boundary_break(self):
        rel_path = 'data/string_break/boundary_break.txt'
        data_path = os.path.join(CUR_SCRIPT_PATH, rel_path)
        with codecs.open(data_path, encoding='utf8') as fp:
            ans = fp.read()

        res = df.test_boundary_break(False)

        self.assertEqual(ans, res)


class TestAutoClip(TestBase):

    def test_3lines_clip(self):
        rel_path = 'data/auto_clip/by_lines.txt'
        data_path = os.path.join(CUR_SCRIPT_PATH, rel_path)
        with codecs.open(data_path, encoding='utf8') as fp:
            ans = fp.read()

        res = df.test_3lines_clip(False)

        self.assertEqual(ans, res)

    def test_no_room(self):
        rel_path = 'data/auto_clip/no_room.txt'
        data_path = os.path.join(CUR_SCRIPT_PATH, rel_path)
        with codecs.open(data_path, encoding='utf8') as fp:
            ans = fp.read()

        res = df.test_autoclip_no_room(False)

        self.assertEqual(ans, res)


class TestDict(TestBase):

    def test_ordered_keys(self):
        rel_path = 'data/dict/foo.txt'
        data_path = os.path.join(CUR_SCRIPT_PATH, rel_path)
        with codecs.open(data_path, encoding='utf8') as fp:
            ans = fp.read()

        res = df.test_dict_ordered_keys(False)

        self.assertEqual(ans, res)


class TestTuple(TestBase):

    def test_ordered_keys(self):
        rel_path = 'data/tuple/simple.txt'
        data_path = os.path.join(CUR_SCRIPT_PATH, rel_path)
        with codecs.open(data_path, encoding='utf8') as fp:
            ans = fp.read()

        res = df.test_tuple(False)

        self.assertEqual(ans, res)


class TestInlineRepr(TestBase):

    def test_inline_repr_out_of_range(self):
        rel_path = 'data/inline_repr/out_of_range.txt'
        data_path = os.path.join(CUR_SCRIPT_PATH, rel_path)
        with codecs.open(data_path, encoding='utf8') as fp:
            ans = fp.read()

        res = df.test_inline_repr_out_of_range(False)

        self.assertEqual(ans, res)


class TestClass(TestBase):

    def test_class_last_el(self):
        rel_path = 'data/class/last_el.txt'
        data_path = os.path.join(CUR_SCRIPT_PATH, rel_path)
        with codecs.open(data_path, encoding='utf8') as fp:
            ans = fp.read()

        res = df.test_class_last_el(False)

        self.assertEqual(ans, res)

    def test_class_all_repr_disable(self):
        rel_path = 'data/class/all_repr_disable.txt'
        data_path = os.path.join(CUR_SCRIPT_PATH, rel_path)
        with codecs.open(data_path, encoding='utf8') as fp:
            ans = fp.read()

        res = df.test_class_all_repr_disable(False)

        self.assertEqual(ans, res)

    def test_class_inst_repr_enable(self):
        rel_path = 'data/class/inst_repr_enable.txt'
        data_path = os.path.join(CUR_SCRIPT_PATH, rel_path)
        with codecs.open(data_path, encoding='utf8') as fp:
            ans = fp.read()

        res = df.test_class_inst_repr_enable(False)

        self.assertEqual(ans, res)

if __name__ == '__main__':
    unittest.main()
