# -*- coding:utf-8 -*-

# >> 优先策略
# 正确性优先，尽量正确显示出所有字段，有无法解析的字段立即报错并退出
_PS_CORRECTNESS_FIRST = 1
# 内容优先，尽量保证输出全文，对于无法解析的字段以预置内容代替
# 比如：<CAN NOT PARSE OBJECT>
_PS_CONTENT_FIRST = 2

_AS_ELEMENT_ = 1
_AS_VALUE_ = 2
_AS_LIST_ELEMENT_ = \
    _AS_DICT_ELEMENT_ = \
    _AS_TUPLE_ELEMENT_ = \
    _AS_CLASS_ELEMENT_ = 4
