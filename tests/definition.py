# -*- coding:utf-8 -*-

def f(): pass

class CE: pass
class CE2(object): pass

class c: 
    def mth():pass
    static_props = 1

class c2(object): 
    def mth():pass
    static_props = 1
    lists = []
    dicts = {}

ic = c()
ic2 = c2()

values = [
    1,
    1.1,
    "s",
    u"us",
    "a中文",
    u"a中文",
    [1],
    (1,2),
    f,
    CE,
    CE2,
    c,
    c2,
    ic,
    ic2,
    ic.mth,
    ic2.mth,
    {
        'key': [],
        u'key2': {},
    },
]
