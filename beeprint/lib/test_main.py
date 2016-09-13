# -*- coding:utf-8 -*-

import unittest

import search_up_tree as sut


class TestUtils(unittest.TestCase):

    def setUp(self):
        pass

    def test_sut(self):

        h = {
            'all': {
                'string': {
                    'bytes': {},
                    'unicode': {},
                    'literal': {},
                },
                'undefined': {},
            },
        }
        sut_tree = sut.Tree(h, {'string': 'hit_string'})
        self.assertEqual(sut_tree.fetch_up('string'), 'hit_string')
        self.assertEqual(sut_tree.fetch_up('literal'), 'hit_string')
        self.assertEqual(sut_tree.fetch_up('undefined'), None)
        self.assertEqual(sut_tree.fetch_up('all'), None)

if __name__ == '__main__':
    unittest.main()
