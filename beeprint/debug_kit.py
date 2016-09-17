# -*- coding:utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division

import inspect
import sys
import re

from . import constants as C
from .utils import print_exc_plus, get_name, has_parent_class


### global variables
G_leading_char = '  '

def add_leading(depth, text):
    text = G_leading_char*depth + text
    text = text.replace('\n', '\n' + G_leading_char*depth)
    return text

def debug(config, level, depth, text):
    if config.debug_level >= level:
        frame_list = inspect.stack()
        frame_obj = frame_list[1][0]
        class_name = frame_obj.f_locals['self'].__class__.__name__
        caller_name = frame_list[1][3]
        depth = len(frame_list) - 6
        if level == C._DL_FUNC_:
            depth -= 1
            text = class_name + '.' + caller_name + ': ' + text
        text = add_leading(depth, text)
        config.debug_stream.write(text + '\n')

def print_obj_path():
    tb = sys.exc_info()[2]
    print()
    # print_exc_plus()

    # >> get traceback frame list
    while True: 
        if not tb.tb_next:
            break
        tb = tb.tb_next

    stack = []
    f = tb.tb_frame
    while f:
        stack.append(f)
        f = f.f_back
    stack.reverse()

    # >> get caller frame info to find variable passed to pp()
    caller_frameinfo = None
    for frame in stack:
        fi = inspect.getframeinfo(frame)
        if fi.filename.endswith("printer.py"):
            break
        caller_frameinfo = fi
    groups = re.search(".*pp\((.*),.*\).*", caller_frameinfo.code_context[0])
    passed_arg_name = groups.group(1)

    # >> get subclass of Block and ctx.obj
    trace = []
    trace_cnt = 0
    repeat = {}
    for frame in stack:
        self = frame.f_locals.get('self')
        if (not self 
                or id(self) in repeat
                or get_name(self) == 'Block'
                or not has_parent_class(self, 'Block')
                ):
            continue
        repeat[id(self)] = True
        obj = self.ctx.obj
        trace.append((self, obj))

    if len(trace) == 0:
        return

    s_trace = passed_arg_name
    print(s_trace, end='')
    last = trace[0][1]
    trace = trace[1:-1]
    for info in trace:
        obj = info[1]
        pos = ''
        if last == obj:
            continue
        if isinstance(last, (tuple, list)):
            pos = "index:%s" % last.index(obj)
            last = obj
        elif isinstance(last, dict):
            pos = "key:%s" % repr(obj[0])
            last = obj[1]
        else:
            # last object is a class or a object
            # according to beeprint block's process:
            #
            # object(A):
            #   K1: V1
            #
            # when last = A, 
            # first time obj = (K1, V1)
            # second time obj = V1
            pos = "attr:%s" % repr(obj[0])
            last = obj[1] # next loop, it would be last == obj
        n = " -> " + pos
        print(n, end='')
        s_trace += n

    return s_trace


def print_frame(f, limit=160):
    attrs = [attr for attr in dir(f) if not attr.startswith('__')]
    for attr in attrs:
        info = repr(getattr(f, attr))
        print("%s: %s" % (attr, info[:limit]))
    print()


