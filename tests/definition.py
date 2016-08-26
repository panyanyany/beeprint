# -*- coding:utf-8 -*-

def EmptyFunc(): pass

class EmptyClassOldStyle: pass
class EmptyClassNewStyle(object): pass

class NormalClassOldStyle: 
    def mth():pass
    static_props = 1

class NormalClassNewStyle(object): 
    def mth():pass
    static_props = 1
    lists = []
    dicts = {}
    tupl = (1,2)

inst_of_normal_class_old_style = NormalClassOldStyle()
inst_of_normal_class_new_style = NormalClassNewStyle()

long_text_en = """
The sky and the earth were at first one blurred entity like an egg. Pangu was born into it.
 
The separation of the sky and the earth took eighteen thousand years-the yang which was light and pure rose to become the sky, and the yin which was heavy and murky（朦胧的） sank to form the earth. Between them was Pangu, who went through nine changes every day, his wisdom greater than that of the sky and his ability greater than that of the earth. Every day the sky rose ten feet higher, the earth became ten feet thicker, and Pangu grew ten feet taller.
 
Another eighteen thousand years passed, and there was an extremely high sky, an extremely thick earth, and an extremely tall Pangu. After Pangu died, his head turned into the Five Sacred Mountains (Mount Tai, Mount Heng, Mount Hua, Mount Heng, Mount Song), his eyes turned into the moon and the sun, his blood changed into water in river and sea, his hair into grass.
 
In all, the universe and Pangu combine in one.
"""

long_text_cn = """
据民间神话传说古时盘古生在黑暗团中，他不能忍受黑暗，用神斧劈向四方，逐渐使天空高远，大地辽阔。他为不使天地会重新合并，继续施展法术。每当盘古的身体长高一尺，天空就随之增高一尺，经过1.8万多年的努力，盘古变成一位顶天立地的巨人，而天空也升得高不可及，大地也变得厚实无比。盘古生前完成开天辟地的伟大业绩，死后永远留给后人无穷无尽的宝藏，成为中华民族崇拜的英雄。
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
    }
]
