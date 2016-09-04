# -*- coding:utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
import sys
import types


from . import constants as C
from . import utils

# >> coding
encoding = 'utf-8'

# >> representation
max_depth = 5
leading = u'  '
newline = False
tuple_in_line = True
list_in_line = True

# >> buffer
buffer_handler = sys.stdout
# use buffer_handler.flush() every print
write_to_buffer_when_execute = False

# >> class control
# 过滤以 x 开头的属性
prop_leading_filters = ["__", "func_"]
# 根据类型过滤对象的属性
prop_filters = [utils.is_pan_function, 'im_func', 'im_self', 'im_class']

# >> 优先策略
# to raise exception or not when errors happened
# _PS_CONTENT_FIRST will keep content printing despite of any error
priority_strategy = C._PS_CONTENT_FIRST

# debug = False
debug_level = 0

# >> string control
# united_str_coding_representation
# In spite of python version
# unicode string will be displayed as u''
# non-unicode string will be displayed as b''
united_str_coding_representation = True
str_display_not_prefix_u = True
str_display_not_prefix_b = True
str_display_escape_special_char = True

element_display_last_with_comma = True

# >> long string control
text_wrap_enable = True
text_wrap_method = C._TEXT_WRAP_BY_TERMINAL
text_wrap_width = 80

# >> content overflow control
