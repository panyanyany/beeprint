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

inst_of_normal_class_old_style = NormalClassOldStyle()
inst_of_normal_class_new_style = NormalClassNewStyle()

values = [
    1,
    1.1,
    "s",
    u"us",
    "a中文",
    u"a中文",
    [1],
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
        u'key2': {},
    },
]
