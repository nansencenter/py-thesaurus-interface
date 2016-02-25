'''
Created on Feb 25, 2016

@author: alevin
'''
from __future__ import absolute_import

import unittest
from pythesint.vocabulary import Vocabulary
from mock.mock import MagicMock


class VocabularyTest(unittest.TestCase):

    def setUp(self):
        self.cat = {'Category': 'Animal', 'Type': 'Cat'}
        self.dog = {'Category': 'Animal', 'Type': 'Dog'}
        self.mouse = {'Category': 'Animal', 'Type': 'Mouse'}
        self.house = {'Category': 'Construction', 'Type': 'house'}

    def test_find_keyword_get_list_not_implemented(self):
        vocab = Vocabulary('VOCAB MOCK')
        with self.assertRaises(NotImplementedError):
            vocab.find_keyword('an item')

    def test_find_keyword_not_found(self):
        vocab = Vocabulary('VOCAB MOCK')
        vocab.get_list = MagicMock(return_value=[self.cat, self.dog,
                                                 self.mouse])
        with self.assertRaises(IndexError):
            vocab.find_keyword('Horse')

    def test_find_keyword(self):
        vocab = Vocabulary('VOCAB MOCK')
        vocab.get_list = MagicMock(return_value=[self.cat, self.dog,
                                                 self.mouse, self.house])
        self.assertDictEqual(vocab.find_keyword('dog'), self.dog)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
