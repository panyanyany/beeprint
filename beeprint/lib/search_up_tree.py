# -*- coding:utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division


class Tree(object):
    
    def __init__(self, adict, values):
        self.d_node_by_name = {}
        self.build_tree(adict, -99999, self.d_node_by_name)
        self.values = values

    def build_tree(self, adict, root_name, d_node_by_name):
        if root_name in adict:
            raise Exception("root name conflicts with keys")

        for k, v in adict.items():
            if k in d_node_by_name:
                raise Exception("invalid dict -- all keys must be unique")
            
            d_node_by_name[k] = root_name
            self.build_tree(v, k, d_node_by_name)

    def fetch_up(self, name):
        if name in self.values:
            return self.values[name]
        if name not in self.d_node_by_name:
            return None
        parent_name = self.d_node_by_name[name]
        return self.fetch_up(parent_name)
