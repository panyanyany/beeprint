# -*- coding:utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
import inspect
import sys
import types
import traceback


_unicode = None
if sys.version_info < (3, 0):
    pyv = 2
    _unicode = unicode
else:
    pyv = 3
    _unicode = str

def is_class_method(name, val):
    if pyv == 2:
        return isinstance(val, types.MethodType) and val.im_self is None
    elif pyv == 3:
        # in python 2, a class method is unbound method type
        # in python 3, a class method is function type as well as a function
        raise Exception("python 3 only has function type and bound method type")

def is_instance_method(name, val):
    if pyv == 3:
        return inspect.ismethod(val)
    elif pyv == 2:
        return isinstance(val, types.MethodType) and val.im_self is not None

def is_pan_function(name, val):
    """detect pan-function which including function and bound method in python 3
    function and unbound method and bound method in python 2
    """
    return inspect.isfunction(val) or inspect.ismethod(val) or inspect.isbuiltin(val)

def print_exc_plus():
    """
    Print the usual traceback information, followed by a listing of all the
    local variables in each frame.
    """
    tb = sys.exc_info()[2]
    while 1:
        if not tb.tb_next:
            break
        tb = tb.tb_next
    stack = []
    f = tb.tb_frame
    while f:
        stack.append(f)
        f = f.f_back
    stack.reverse()
    traceback.print_exc()
    print("Locals by frame, innermost last")
    for frame in stack:
        print()
        print("Frame %s in %s at line %s" % (frame.f_code.co_name,
                                             frame.f_code.co_filename,
                                             frame.f_lineno))
        for key, value in frame.f_locals.items():
            print("\t%20s = " % key, end='')
            # We have to be careful not to cause a new error in our error
            # printer! Calling str() on an unknown object could cause an
            # error we don't want.
            try:
                print(value)
            except:
                print("<ERROR WHILE PRINTING VALUE>")

def is_newline_obj(o):
    if hasattr(o, '__module__'):
        return True
    return False

def is_class_instance(o):
    # print('%s: class instance: %s' % (inspect.isclass(o), o))
    if o is None:
        return False
    try:
        # to detect:
        # old-style class & new-style class
        # instance of old-style class and of new-style class
        # method of instance of both class
        # function

        # o.__module__ in python 3.5 some instance has no this attribute

        if (inspect.isclass(o)
            or inspect.isfunction(o)
            or inspect.ismethod(o)):
            return False
        if isinstance(o, (int, float, list, tuple, dict, str, _unicode)):
            return False
        return True
    except:
        pass
    return False

def is_class(o):
    # print('%s: class: %s' % (inspect.isclass(o), o))
    return inspect.isclass(o)

    if is_class_instance(o) or inspect.isfunction(o) or inspect.isbuiltin(o) or inspect.ismethod(o):
        return False

    return True

def get_name(o):
    if hasattr(o, '__name__'):
        return o.__name__
    if hasattr(o, '__class__'):
        return o.__class__.__name__

    raise Exception("%s" % type(o))

def has_parent_class(obj, parent_name):
    if hasattr(obj, '__mro__'):
        mro = obj.__mro__
    elif hasattr(obj, '__class__'):
        mro = obj.__class__.__mro__
    else:
        return False

    for cls in mro:
        cls_name = get_name(cls)
        if cls_name.endswith(parent_name):
            return True
    return False


def has_custom_repr(o):
    repr_typ_name = lambda o: type(o.__repr__).__name__
    builtin_repr_names = ['method-wrapper', 'wrapper_descriptor', 'method-wrapper']
    return hasattr(o, '__repr__') and (repr_typ_name(o) not in builtin_repr_names)


def get_type(o):
    if is_class_instance(o):
        label = 'instance'
    elif inspect.isfunction(o):
        label = 'function'
    elif inspect.isbuiltin(o):
        label = 'builtin'
    elif inspect.ismethod(o):
        label = 'method'
    else:
        '本身就是类，不是对象'
        label = 'class'

    return label


def is_base_type(o):
    return isinstance(o, (list, tuple, dict, int, float, str, _unicode))
