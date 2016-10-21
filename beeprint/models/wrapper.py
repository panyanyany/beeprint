# -*- coding:utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division

from beeprint import constants as C
from ..utils import pyv


class Wrapper(object):

    def get_prefix(self):
        pass

    def get_suffix(self):
        pass

    def wrap(self, obj):
        pass


class StringWrapper(Wrapper):

    def __init__(self, config, typ, lqm=None, rqm=None, etm=None):

        self.config = config
        # ReprType
        self.typ = typ
        # left_quotation_mark
        self.lqm = lqm or config.str_display_lqm
        # right_quotation_mark
        self.rqm = rqm or config.str_display_rqm
        # encode type mark
        self.etm = etm

        if self.etm is None:
            typ = self.typ
            self.etm = ''
            if typ.is_all(typ._UNICODE_):
                if self.config.str_display_not_prefix_u:
                    pass
                else:
                    if pyv == 2:
                        self.etm = u'u'
                    else:
                        pass
            elif typ.is_all(typ._BYTES_):
                # in py3, printed string will enclose with b''
                if self.config.str_display_not_prefix_b:
                    pass
                else:
                    if pyv == 2:
                        pass
                    else:
                        self.etm = u'b'

    def wrap(self, obj):
        return ''.join([
            self.etm,
            self.lqm,
            obj,
            self.rqm,
        ])

    def get_prefix(self):
        return self.etm + self.lqm

    def get_suffix(self):
        return self.rqm
