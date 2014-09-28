#-*- coding:utf-8 -*-
import sys, traceback, types
import inspect

outfile = sys.stdout
encoding = 'utf-8'
maxDeep = 2
leading = u'  '
newline = False
write_to_buffer_when_execute = False
bufferHandle = sys.stdout
tuple_in_line = True
list_in_line = True

_AS_ELEMENT_ = 1
_AS_VALUE_ = 2
_AS_LIST_ELEMENT_ = _AS_DICT_ELEMENT_ = _AS_TUPLE_ELEMENT_ = _AS_CLASS_ELEMENT_ = 4

def object_attr_default_filter(obj, name, val):
    '过滤不需要的对象属性'

    return False

    if name.startswith("__") or name.startswith("func_"):
        return True
    elif type(val) == types.MethodType:
        return True

    return False


def dict_key_filter(obj, name, val):
    return False


def _b(s):
    if write_to_buffer_when_execute:
        bufferHandle.write(s)
        bufferHandle.flush()
    return s

def pstr(s):
    res = u''
    
    if isinstance(s, unicode):
        res += s
    elif isinstance(s, str):
        try:
            res += s.decode(encoding)
        except Exception, e:
            #print "%s, %s, %s" % (type(s), type(''), encoding)
            raise e
            #res += s.decode('gbk')

    else:
        res += str(s).decode(encoding)

    return res

def dump_obj(o, output = True):
    
    res = build_single_block(o, 0)
    if output and not write_to_buffer_when_execute:
        try:
            print res,
        except Exception, e:
            print_exc_plus()
    else:
        return res

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
    print "Locals by frame, innermost last"
    for frame in stack:
        print
        print "Frame %s in %s at line %s" % (frame.f_code.co_name,
                                             frame.f_code.co_filename,
                                             frame.f_lineno)
        for key, value in frame.f_locals.items():
            print "\t%20s = " % key,
            #We have to be careful not to cause a new error in our error
            #printer! Calling str() on an unknown object could cause an
            #error we don't want.
            try:                   
                print value
            except:
                print "<ERROR WHILE PRINTING VALUE>"
        

def tail_symbol(position):
    if (position & _AS_LIST_ELEMENT_ or 
        position & _AS_DICT_ELEMENT_ or
        position & _AS_CLASS_ELEMENT_ or
        position & _AS_TUPLE_ELEMENT_):
        tail = ','
    else:
        tail = ''
    return tail



def build_single_block(obj, leadCnt = 0, position = _AS_ELEMENT_):
    '遍历对象，判断对象内成员的类型，然后调用对应的 build_*_block() 处理'
    ret = pstr('')

    tail = tail_symbol(position)

    if maxDeep < leadCnt:
        if newline or position & _AS_ELEMENT_:
            ret = pstr(leadCnt * leading) + pstr("<OUT OF RANGE>\n")
        else:
            ret = pstr(" ") + pstr("<OUT OF RANGE>\n")
        if position & _AS_LIST_ELEMENT_:
            ret = ret[:-1] + pstr(tail + "\n")
        return _b(ret)

    if isinstance(obj, dict):
        ret += build_dict_block(obj, leadCnt, position)
    elif isinstance(obj, list):
        ret += build_list_block(obj, leadCnt, position)
    elif isinstance(obj, tuple):
        ret += build_tuple_block(obj, leadCnt, position)
    elif is_extendable(obj):#hasattr(obj, '__dict__') or isinstance(obj, object):
        ret += build_class_block(obj, leadCnt, position)
    else:
        ret += _b(leadCnt * leading + typeval(obj) + pstr(tail + '\n'))


    return ret

def is_extendable(obj):
    '判断obj是否可以展开'
    return isinstance(obj, dict) or hasattr(obj, '__dict__') or isinstance(obj, (tuple, list, types.FrameType))

def build_pair_block(name, val, leadCnt = 0, position = _AS_ELEMENT_):
    ret = pstr('')

    tail = tail_symbol(position)

    ret += _b(leading*leadCnt + typeval(name) + ':')
    if is_extendable(val) and maxDeep > leadCnt:
        if newline or isinstance(val, (types.InstanceType, types.FunctionType)):
            ret += _b(pstr('\n'))
            leadCnt = leadCnt+1
        else:
            ret += _b(pstr(" "))

        ret += build_single_block(val, leadCnt, _AS_VALUE_)
    else:
        if maxDeep <= leadCnt:
            ret += _b(pstr(" <OUT OF RANGE>%s\n" % tail))
        else:
            ret += _b(pstr(" ") + typeval(val) + pstr(tail + '\n'))
    return ret

def build_string_block(s, leadCnt = 0):
    return _b(leadCnt*leading + typeval(s) + pstr('\n'))

def build_list_block(o, leadCnt = 0, position = _AS_VALUE_):
    ret = pstr('')

    tail = tail_symbol(position)

    '所有元素显示在同一行'
    if list_in_line:
        _f = map(lambda e: not is_extendable(e), o)
        if all(_f):
            _o = map(lambda e: typeval(e), o)
            if newline or position & _AS_ELEMENT_:
                ret += pstr(leading*leadCnt)
            ret += pstr("[") + ', '.join(_o) + pstr("]%s\n" % tail)
            return _b(ret)

    # [
    if newline or position & _AS_ELEMENT_:
        ret += _b(leading*leadCnt + pstr('[\n'))
    else:
        ret += _b(pstr('[\n'))

    # body
    for e in o:
        ret += build_single_block(e, leadCnt+1, _AS_ELEMENT_ | _AS_LIST_ELEMENT_)

    # ]
    ret += _b(leading*leadCnt + pstr(']%s\n' % tail))

    return ret

def build_tuple_block(o, leadCnt = 0, position = _AS_VALUE_):
    ret = pstr('')

    tail = tail_symbol(position)

    if tuple_in_line:
        _f = map(lambda e: not is_extendable(e), o)
        if all(_f):
            _o = map(lambda e: typeval(e), o)
            ret += _b(pstr("(") + ', '.join(_o) + ')%s\n' % tail)
            return ret

    # (
    if newline or position & _AS_ELEMENT_:
        ret += _b(leading*leadCnt + pstr('(\n'))
    else:
        ret += _b(pstr('(\n'))

    # body
    for e in o:
        ret += build_single_block(e, leadCnt+1, _AS_ELEMENT_ | _AS_TUPLE_ELEMENT_)

    # )
    ret += _b(leading*leadCnt + pstr(')%s\n' % tail))

    return ret

def build_dict_block(o, leadCnt = 0, position = _AS_VALUE_):
    ret = pstr('')

    tail = tail_symbol(position)
    # {
    if newline or position & _AS_ELEMENT_:
        ret += _b(leading*leadCnt + pstr('{')+pstr('\n'))
    else:
        ret += _b(pstr('{')+pstr('\n'))

    # body
    for k in o:
        v = o[k]
        if dict_key_filter(o, k, v):
            continue
        #ret += leading*(leadCnt + 1) + typeval(k) + pstr(": ")
        #ret += build_single_block(v, leadCnt+1)
        ret += build_pair_block(k, v, leadCnt + 1)

    # }
    ret += _b(leading*leadCnt + '}' + pstr(tail + '\n'))
            
    return ret

def build_class_block(o, leadCnt = 0, position = _AS_ELEMENT_):
    ret = pstr('')

    # {
    _leading = leading * leadCnt

    if hasattr(o, '__class__'):
        ret += _b(_leading + pstr('object(%s):'%o.__class__.__name__)+pstr('\n'))
    else:
        '本身就是类，不是对象'
        ret += _b(_leading + pstr('class(%s):'%o.__name__)+pstr('\n'))


    # body
    props = dir(o)
    props_cnt = len(props)
    for idx, attr in enumerate(props):
        if attr == '__abstractmethods__':
            continue
        val = getattr(o, attr)
        '过滤不需要的属性'
        if object_attr_default_filter(o, attr, val):
            continue

        '最后一个元素不需要再加(,)逗号'
        if idx == props_cnt - 1:
            position = _AS_VALUE_
        else:
            position = _AS_CLASS_ELEMENT_

        #'忽略掉 以__开头的成员、自引用成员、函数成员'
        ret += build_pair_block(attr, val, leadCnt+1, position)


    # }
    #ret += leading*leadCnt + '}' + pstr('\n')
    return ret

def typeval(v):
    #print "%s, %s, %s, %s" % (v, type(v), type(''), encoding)
    try:
        m = pstr(v).replace(u'\n', u'\\n')
        m = m.replace(u'\r', u'\\r')

        if isinstance(v, str):
            ret = pstr('"') + m + pstr('"')
        elif isinstance(v, unicode):
            ret = pstr('u\'') + m + pstr('\'')
        else:
            ret = pstr(v)
    except Exception, e:
        ret = pstr("<CAN NOT PARSE OBJECT>")

    return ret

class testcls2:
    def __init__(self):
        self.t1 = 't1'
        self.t2 = 't三'
class testcls:
    a = 'aaaa'
    b = 'bbbb'
    c = '三三三'
    def __init__(self):
        self.p1 = 'p1'
        self.p2 = 222
        self.p3 = testcls2()
        self.f = typeval
        self.p4 = {
            'a': 'va',
            'u': u'unicode',
            '键': '值',
            'i': 123,
            'list': ['值值', 1, 1.3],
            'tuple': ('中文', 3, 3.4, testcls2()),
            'obj': testcls2()
        }
    def func(self):
        pass

if __name__ == '__main__':

    newline = False
    bufferHandle = open("../tmps/tools/dump.test", "w+")
    tuple_in_line = False
    list_in_line = True
    maxDeep = 3
    try:
        t = testcls()
        #print dir(testcls)
        #print
        #print dir(t)
        #print
        #print t.__dict__
        #print
        #dump_obj('a')
        #dump_obj('哈哈')
        #dump_obj({'a':1, 'b':2, 'c':[2,3]})
        #dump_obj(t)
        dump_obj(typeval)
        open("afdasfa/fasdfasf")
    except Exception as e:
        print e
        #print dump_obj(inspect.trace())
