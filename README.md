dump.py  
=======  
  
var_dump() of python, format your output | python 中的 var_dump()，用于打印 Python 数据结构，类似于 pprint  
  
对于一个dict，它输出如下：  

	{  
	  'a': 1  
	  'c':   
	    [  
	      2,  
	      3,  
	    ]  
	  'b': 2  
	}  
对于一个object，它输出如下： 

	object(testcls):  
	  'a': 'aaaa'  
	  'b': 'bbbb'  
	  'c': '三三三'  
	  'p1': 'p1'  
	  'p2': 222  
	  'p3':   
	    object(testcls2):  
	      't1': 't1'  
	      't2': 't三'  
	  'p4':   
	    {  
	      'a': 'va'  
	      '键': '值'  
	      'obj':   
	        object(testcls2):  
	          't1': 't1'  
	          't2': 't三'  
	      'tuple':   
	        (  
	          '中文',  
	          3,  
	          3.4,  
	        )  
	      'i': 123  
	      'list':   
	        [  
	          '值值',  
	          1,  
	          1.3,  
	        ]  
	      'u': u'unicode'  
	    }  
示例解释：  

	object(testcls):  
	  ...  
	  'p3':   
	    object(testcls2):  
	      't1': 't1'  
	      't2': 't三'  
	  ...  
在这里 p3 是 testcls 类实例的一个属性，所以它比 testcls 要多缩进一格，表示从属于。  
而 p3 的值（testcls2类的实例）也是一个对象，而这个对象属于 p3，所以它比 p3 多缩进一格。  
若 p3 的值的结构仅仅是字符串、数字等单行结构，那么它就不用空行再缩进。而是直接跟在 p3 后面。例如 p2。  
