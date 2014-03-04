#-*- coding:utf-8 -*-
import sys, traceback, types
from PFileUtl import file_put_contents

outfile = sys.stdout
encoding = 'utf-8'
maxDeep = 7
leading = u'  '
newline = True
output_when_execute = False

def object_attr_default_filter(obj, name, val):
	'过滤不需要的对象属性'
	if name.startswith("__") or name.startswith("func_"):
		return True
	elif type(val) == types.MethodType:
		return True

	return False

def _output_s(s):
	if output_when_execute:
		print s,
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
	
	res = build_single_block(o)
	if output and not output_when_execute:
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
        

def build_single_block(obj, leadCnt = 0):
	'遍历对象，判断对象内成员的类型，然后调用对应的 build_*_block() 处理'
	ret = pstr('')
	if maxDeep < leadCnt:
		return pstr("<OUT OF RANGE>")

	try:
		if isinstance(obj, dict):
			#print type(obj)
			ret += build_dict_block(obj, leadCnt)
		elif hasattr(obj, '__dict__'):
			ret += build_class_block(obj, leadCnt)
		elif isinstance(obj, list):
			ret += build_list_block(obj, leadCnt)
		elif isinstance(obj, tuple):
			ret += build_tuple_block(obj, leadCnt)
		else:
			#if not pair: ret += leadCnt * leading
			ret += _output_s(leadCnt * leading + typeval(obj) + pstr('\n'))
	except Exception, e:
		#print "Error Caught When Building Object, Current Built String is: " + ret
		#print_exc_plus()
		#print "=="*8
		pass

	return ret

def is_extendable(obj):
	'判断obj是否可以展开'
	return isinstance(obj, dict) or hasattr(obj, '__dict__') or isinstance(obj, (tuple, list))

def build_pair_block(name, val, leadCnt = 0):
	ret = pstr('')

	ret += _output_s(leading*leadCnt + typeval(name) + ': ')
	if is_extendable(val):
		ret += _output_s(pstr('\n'))
		ret += build_single_block(val, leadCnt+1)
	else:
		ret += _output_s(typeval(val) + pstr('\n'))
	return ret

def build_string_block(s, leadCnt = 0):
	return _output_s(leadCnt*leading + typeval(s) + pstr('\n'))

def build_list_block(o, leadCnt = 0):
	ret = pstr('')

	# [
	ret += _output_s(leading*leadCnt + pstr('[\n'))

	# body
	for e in o:
		ret += build_single_block(e, leadCnt+1)[:-1] + pstr(',\n')

	# ]
	ret += _output_s(leading*leadCnt + pstr(']\n'))

	return ret

def build_tuple_block(o, leadCnt = 0):
	ret = pstr('')

	# (
	ret += _output_s(leading*leadCnt + pstr('(\n'))

	# body
	for e in o:
		ret += build_single_block(e, leadCnt+1)[:-1] + pstr(',\n')

	# )
	ret += _output_s(leading*leadCnt + pstr(')\n'))

	return ret

def build_dict_block(o, leadCnt = 0):
	ret = pstr('')

	# {
	ret += _output_s(leading*leadCnt + pstr('{')+pstr('\n'))

	# body
	for k in o:
		v = o[k]
		#ret += leading*(leadCnt + 1) + typeval(k) + pstr(": ")
		#ret += build_single_block(v, leadCnt+1)
		ret += build_pair_block(k, v, leadCnt + 1)

	# }
	ret += _output_s(leading*leadCnt + '}' + pstr('\n'))
			
	return ret

def build_class_block(o, leadCnt = 0):
	ret = pstr('')

	# {
	ret += _output_s(leading*leadCnt + pstr('object(%s):'%o.__class__.__name__)+pstr('\n'))

	# body
	for attr in dir(o):
		val = getattr(o, attr)
		'过滤不需要的属性'
		if object_attr_default_filter(o, attr, val):
			continue
		'忽略掉 以__开头的成员、自引用成员、函数成员'
		if attr.startswith('__') or attr.startswith('im_') or hasattr(val, 'im_func'):
			ret += build_pair_block(attr, str(val), leadCnt+1)
		else:
			ret += build_pair_block(attr, val, leadCnt+1)


	# }
	#ret += leading*leadCnt + '}' + pstr('\n')
	return ret

def typeval(v):
	#print "%s, %s, %s, %s" % (v, type(v), type(''), encoding)
	try:
		m = pstr(v).replace(u'\n', u'\\n')
		m = m.replace(u'\r', u'\\r')

		if isinstance(v, str):
			ret = pstr('\'') + m + pstr('\'')
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
		self.p4 = {
			'a': 'va',
			'u': u'unicode',
			'键': '值',
			'i': 123,
			'list': ['值值', 1, 1.3],
			'tuple': ('中文', 3, 3.4),
			'obj': testcls2()
		}
	def func(self):
		pass

if __name__ == '__main__':
	t = testcls()
	#print dir(testcls)
	#print
	#print dir(t)
	#print
	#print t.__dict__
	#print
	dump_obj('a')
	dump_obj('哈哈')
	dump_obj({'a':1, 'b':2, 'c':[2,3]})
	dump_obj(t)
	#file_put_contents('deprint.log', dump_obj(t).encode('gbk'))
