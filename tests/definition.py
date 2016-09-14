# -*- coding:utf-8 -*-
from beeprint import constants as C 
from beeprint import pp
from beeprint import Config

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
    config = Config()
    config.string_break_method = C._STRING_BREAK_BY_WIDTH
    return pp(v_line_break_boundary, output, config=config)


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
    config = Config()
    config.max_depth = 1
    return pp(out_of_range, output, config=config)

out_of_range_in_dict = {
    'one': inst_of_normal_class_new_style,
    'two': inst_of_normal_class_new_style,
}

def test_out_of_range_in_dict(output=True):
    config = Config()
    config.max_depth = 1
    return pp(out_of_range_in_dict, output, config=config)

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
    config = Config()
    config.dict_ordered_key_enable = True
    return pp(dict_multi_keys, output, config=config)


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


def test_class(output=True):
    config = Config()
    return pp(EmptyClassNewStyle, output, config=config)

sort_of_string = [
    'normal',
    u'unicode',
    b'\xff\xfe',
    '\xff\xfe',
]

def test_sort_of_string(output=True):
    config = Config()
    return pp(sort_of_string, output, config=config)


class ReprMethodClassNewStyle(object):
    def __repr__(self):
        return "<Hey I'm ReprMethodClassNewStyle>"

def test_class_last_el(output=True):
    config = Config()
    # config.debug_level = 9
    rm = ReprMethodClassNewStyle()
    nc = NormalClassNewStyle()
    return pp([rm, nc, rm], output, config=config)
