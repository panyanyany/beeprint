# -*- coding:utf-8 -*-
from __future__ import print_function
from beeprint import constants as C 
from beeprint import pp
from beeprint import Config
from beeprint.helper import ustr
from pprintpp import pprint as ppp

def EmptyFunc(): pass

class EmptyClassOldStyle: pass
class EmptyClassNewStyle(object): pass

class NormalClassOldStyle: 
    def mth():pass
    static_props = 1

class NormalClassNewStyle(object): 
    def __init__(self):
        self.say_hi = 'hello world'
    def mth():pass
    static_props = 1
    lists = []
    dicts = {}
    tupl = (1,2)

inst_of_normal_class_old_style = NormalClassOldStyle()
inst_of_normal_class_new_style = NormalClassNewStyle()

# there are tabs here!!
long_text_en = """
The sky and the earth were at first one blurred entity like an egg. Pangu was born into it.
 
	The separation of the sky and the earth took eighteen thousand years-the yang which was light and pure rose to become the sky, 	and the yin which was heavy and murky（朦胧的） sank to form the earth. Between them was Pangu, who went through nine 	changes every day, his wisdom greater than that of the sky and his ability greater than that of the earth. Every day the sky rose ten feet higher, the earth became ten feet thicker, and Pangu grew ten feet taller.
 
Another eighteen thousand years passed, and there was an extremely high sky, an extremely thick earth, and an extremely tall Pangu. After Pangu died, his head turned into the Five Sacred Mountains (Mount Tai, Mount Heng, Mount Hua, Mount Heng, Mount Song), his eyes turned into the moon and the sun, his blood changed into water in river and sea, his hair into grass.
 
In all, the universe and Pangu combine in one.
"""

# there are tabs here!!
long_text_cn = """
据民间神话传说古时盘古生在黑暗团中，他不能忍受黑暗，用神斧劈向四方，逐渐使天空高远，大地辽阔。
	他为不使天地会重新合并，继续施展法术。每当盘古的身体长高一尺，天空就随之增高一尺，
	经过1.8万多年的努力，盘古变成一位顶天立地的巨人，而天空也升得高不可及，大地也变得厚实无比。盘古生前完成开天辟地的伟大业绩，死后永远留给后人无穷无尽的宝藏，成为中华民族崇拜的英雄。
"""

long_text_in_list = [
    [
        long_text_en,
        long_text_cn,
    ],
]

long_text_in_dict = [
    {"english version": long_text_en},
    {"simplify chinese versino": long_text_cn},
]

short_list = [1, 2, 3, 4, 5, 6]
complicated_list = [
    1,
    [2, ],
    {
        'key': 'val',
    },
]

values = [
    1,
    1.1,
    "literal",
    u"unicode",
    "literal中文",
    u"unicode中文",
    short_list,
    complicated_list,
    (1,2),
    EmptyFunc,
    EmptyClassOldStyle,
    EmptyClassNewStyle,
    NormalClassOldStyle,
    NormalClassNewStyle,
    inst_of_normal_class_old_style,
    inst_of_normal_class_new_style,
    inst_of_normal_class_old_style.mth,
    inst_of_normal_class_new_style.mth,
    {
        'key': [],
    },
    {
        'key': inst_of_normal_class_new_style,
    },
]

v_line_break_boundary = [
    {},
    "boundary testing string: 80col,new line part filled with x ................",
    "boundary testing string: 81col,new line part filled with x ............... x",
    "boundary testing string: 82col,new line part filled with x ............... xx",
]

def test_boundary_break(output=True):
    return pp(v_line_break_boundary, output, string_break_method=C._STRING_BREAK_BY_WIDTH)


out_of_range = [
    'nomarl\t\n1',
    complicated_list,
    EmptyFunc,
    EmptyClassOldStyle,
    EmptyClassNewStyle,
    inst_of_normal_class_old_style,
    inst_of_normal_class_new_style,
]

def test_out_of_range(output=True):
    return pp(out_of_range, output, max_depth=1)

out_of_range_in_dict = {
    'one': inst_of_normal_class_new_style,
    'two': inst_of_normal_class_new_style,
}

def test_out_of_range_in_dict(output=True):
    return pp(out_of_range_in_dict, output, max_depth=1)

clip_by_3_lines = [
    'a'*(77*2 - 2),
    'a'*77*2,
    'a'*77*3,
]


def test_3lines_clip(output=True):
    config = Config()
    config.text_autoclip_enable = True
    config.text_autoclip_method = C._TEXT_AUTOCLIP_BY_LINE
    config.string_break_enable = True
    config.string_break_method = C._STRING_BREAK_BY_WIDTH
    return pp(clip_by_3_lines, output, config=config)


dict_multi_keys = {
    'entities': {
        'hashtags': [], 
        'urls': [
            {
                'display_url': 'tumblr.com/xnr37hf0yz', 
                'expanded_url': 'http://tumblr.com/xnr37hf0yz', 
                'indices': [107, 126], 
                'url': 'http://t.co/cCIWIwg'
            }
        ], 
        'user_mentions': []
    },
}


def test_dict_ordered_keys(output=True):
    return pp(dict_multi_keys, output, dict_ordered_key_enable=True)


def test_complicate_data(output=True):
    config = Config()
    config.string_break_method = C._STRING_BREAK_BY_WIDTH
    config.text_autoclip_enable = False
    res = pp(values, output, config=config)
    res += pp(long_text_in_dict, output, config=config)
    res += pp(long_text_in_list, output, config=config)
    return res

inline_repr = [
    "this string fits 80 col line ..... ..... ..... ..... ..... ..... ..... ....",
    inst_of_normal_class_new_style,
    inst_of_normal_class_new_style.mth,
]

def test_inline_repr_out_of_range(output=True):
    config = Config()
    config.max_depth = 1
    config.string_break_method = C._STRING_BREAK_BY_WIDTH
    config.string_break_width = 40
    return pp(inline_repr, output, config=config)

tuple_testing = (1, {'indict':(1,), 'z': 1},)

def test_tuple(output=True):
    config = Config()
    return pp(tuple_testing, output, config=config)

tuple_nested = (1, (2,))
def test_tuple_nested(output=True):
    config = Config()
    return pp(tuple_nested, output, config=config)

def test_class(output=True):
    config = Config()
    return pp(EmptyClassNewStyle, output, config=config)

sort_of_string = [
    '\\',
    u'\\',
    b'\\',
    u'\\'.encode('utf8'),
]
sort_of_string += [
    'normal',
    u'unicode',
]
sort_of_string += [
    '中文',
    # b'中文',
    u'中文',
    u'中文'.encode('utf8'),
]
sort_of_string += [
    '\xff\xfe',
    b'\xff\xfe',
    u'\xff\xfe',
    u'\xff\xfe'.encode('utf8'),
]
sort_of_string += [
    '\ud800', # different in py2 and py3
    b'\ud800',
    u'\ud800',
    # u'\ud800-\udbff\\\udc00\udc01-\udfff',
]

def test_sort_of_string(output=True):
    config = Config()
    config.debug_delay = False
    config.str_display_not_prefix_u = False
    config.str_display_not_prefix_b = False
    for sstr in sort_of_string:
        ints = ''
        for e in sstr:
            try:
                ints += '%d ' % ord(e)
            except:
                ints += '%d ' % e
        print('%40s %s %s' % (ints, repr(sstr), len(sstr)))
    return pp(sort_of_string, output, config=config)
    # return ppp(sort_of_string)


# >> ReprMethod
class ReprMethodClassOldStyle:
    def __repr__(self):
        return "<Hey I'm %s>" % self.__class__.__name__

class ReprMethodClassNewStyle(object):
    def __repr__(self):
        return "<Hey I'm %s>" % self.__class__.__name__

# >> ReprStatic
class ReprStaticClassOldStyle:
    @staticmethod
    def __repr__():
        return "<Hey I'm static of ReprStaticClassOldStyle>"

class ReprStaticClassNewStyle(object):
    @staticmethod
    def __repr__():
        return "<Hey I'm static of ReprStaticClassNewStyle>"

# >> ReprClassMethod
class ReprClassMethodClassOldStyle:
    @classmethod
    def __repr__(cls):
        return "<Hey I'm %s>" % cls.__name__

class ReprClassMethodClassNewStyle(object):
    @classmethod
    def __repr__(cls):
        return "<Hey I'm %s>" % cls.__name__

# >> ReprLambda
class ReprLambdaClassOldStyle:
    __repr__ = lambda self: "<Hey I'm %s>" % self.__class__.__name__

class ReprLambdaClassNewStyle:
    __repr__ = lambda self: "<Hey I'm %s>" % self.__class__.__name__

def test_class_last_el(output=True):
    config = Config()
    config.instance_repr_enable = False
    rm = ReprMethodClassNewStyle()
    nc = NormalClassNewStyle()
    return pp([rm, nc, rm], output, config=config)


class OuterClass(object):
    class InnerClass(object):
        pass


def test_inner_class(output=True):
    config = Config()
    return pp(OuterClass, output, config=config)


class ForNoRoom(object):
    xxxxxxxxxxxxxxxxxxx = 'ooooooooooooooooooooooo'

autoclip_no_room = [
    ['.'*80, {}],
    {'akey': 'value'*3},
    ForNoRoom,
]

def test_autoclip_no_room(output=True):
    config = Config()
    # config.debug_level = 9
    config.max_depth = 2
    config.string_break_width = 1
    config.string_break_method = C._STRING_BREAK_BY_WIDTH
    return pp(autoclip_no_room, output, config=config)


class_repr = [
    ReprMethodClassOldStyle,
    ReprMethodClassNewStyle,
    ReprStaticClassOldStyle,
    ReprStaticClassNewStyle,
    ReprClassMethodClassOldStyle,
    ReprClassMethodClassNewStyle,
    ReprLambdaClassOldStyle,
    ReprLambdaClassNewStyle,
    EmptyFunc,
    EmptyClassOldStyle,
    EmptyClassNewStyle,
    NormalClassOldStyle,
    NormalClassNewStyle,
]
def test_class_all_repr_disable(output=True):
    return pp(class_repr, output, instance_repr_enable=False)

def test_class_inst_repr_enable(output=True):
    inst_repr = []
    for c in class_repr:
        inst_repr.append(c())
    return pp(class_repr + inst_repr, output)


class RecurTestNormalClass(object):
    k1 = 1

inst_of_recur_normal = RecurTestNormalClass()
inst_of_recur_normal.k2 = inst_of_recur_normal

class RecurTestRecurClass(object):
    k1 = 1
RecurTestRecurClass.k2 = RecurTestRecurClass

def test_recursion(output=True):
    d = {}
    d['d'] = d

    d2 = {'1':1}
    d2['r'] = {'d2':d2}

    l = []
    l.append(l)

    recursive_values = [
        l,
        l, # this one should not be treat as recursion
        d,
        d2,
        inst_of_recur_normal,
        RecurTestRecurClass,
    ]
    return pp(recursive_values, output)
    # return ppp(recursive_values)
