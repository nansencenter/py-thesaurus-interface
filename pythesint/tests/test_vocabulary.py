'''
Created on Feb 25, 2016

@author: alevin
'''
from __future__ import absolute_import

from collections import OrderedDict

import unittest
from mock.mock import MagicMock

from pythesint.vocabulary import Vocabulary


class VocabularyTest(unittest.TestCase):

    def setUp(self):
        self.cat = OrderedDict({'Category': 'Animal', 'Type': 'Cat'})
        self.dog = OrderedDict({'Category': 'Animal', 'Type': 'Dog'})
        self.mouse = OrderedDict({'Category': 'Animal', 'Type': 'Mouse'})
        self.house = OrderedDict({'Category': 'Construction', 'Type': 'House'})
        self.animal = OrderedDict({'Category': 'Animal', 'Type': ''})
        self.test_list = [self.cat, self.dog, self.mouse, self.house, self.animal]

    def test_find_keyword_get_list_not_implemented(self):
        vocab = Vocabulary('VOCAB MOCK')
        with self.assertRaises(NotImplementedError):
            vocab.find_keyword('an item')

    def test_find_keyword_not_found(self):
        vocab = Vocabulary('VOCAB MOCK')
        vocab.get_list = MagicMock(return_value=self.test_list)
        with self.assertRaises(IndexError):
            vocab.find_keyword('Horse')

    def test_find_keyword(self):
        vocab = Vocabulary('VOCAB MOCK')
        vocab.get_list = MagicMock(return_value=self.test_list)
        self.assertEqual(vocab.find_keyword('dog'), self.dog)
        self.assertEqual(vocab.find_keyword('Animal'), self.animal)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
