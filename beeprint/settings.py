# -*- coding:utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
import sys
import types


from . import constants as C

outfile = sys.stdout
encoding = 'utf-8'
maxDeep = 5
leading = u'  '
newline = False
write_to_buffer_when_execute = False
bufferHandle = sys.stdout
tuple_in_line = True
list_in_line = True
# 过滤以 x 开头的属性
prop_leading_filters = ["__", "func_"]
# 根据类型过滤对象的属性
prop_filters = [types.BuiltinFunctionType, types.BuiltinMethodType, 'im_func', 'im_self', 'im_class']

# >> 优先策略
priority_strategy = C._PS_CONTENT_FIRST

# debug = False
debug_level = 0

# united_str_coding_representation
# In spite of python version
# unicode string will be displayed as u''
# non-unicode string will be displayed as b''
united_str_coding_representation = True
