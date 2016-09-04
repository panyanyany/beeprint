# -*- coding:utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division

from collections import OrderedDict


class PositionDict(OrderedDict):

    def __init__(self, tlist):
        idx_by_key = {}
        key_by_idx = {}
        for idx, tup in enumerate(tlist):
            key = tup[0]
            idx_by_key[key] = idx
            key_by_idx[idx] = key

        self.idx_by_key = idx_by_key
        self.key_by_idx = key_by_idx

        super(PositionDict, self).__init__(tlist)

    def idx(self, key):
        return self.idx_by_key[key]

    def indexed_items(self):
        for key, val in super(PositionDict, self).items():
            idx = self.idx(key)
            yield idx, key, val

    def index(self, pair):
        return self.idx(pair[0])

    def __iter__(self):
        for key in super(PositionDict, self).__iter__():
            val = self[key]
            idx = self.idx(key)
            yield idx, key, val
