# -*- coding:utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division


class Walker(object):
    
    class Exit(Exception): pass
    class PrintNExit(Exception): pass
