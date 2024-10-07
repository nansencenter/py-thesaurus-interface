'''
Created on Feb 25, 2016

@author: alevin
'''
from __future__ import absolute_import

from collections import OrderedDict

import unittest
import unittest.mock as mock

from pythesint.vocabulary import Vocabulary


class VocabularyTest(unittest.TestCase):

    def setUp(self):
        self.cat = OrderedDict([('Category', 'Animal'), ('Type', 'Cat'), ('Name', '')])
        self.cat2 = OrderedDict([('Category', 'Animal'), ('Type', 'Cat'), ('Name', 'The cat')])
        self.dog = OrderedDict([('Category', 'Animal'), ('Type', 'Dog'), ('Name', '')])
        self.mouse = OrderedDict([('Category', 'Animal'), ('Type', 'Mouse'), ('Name', '')])
        self.house = OrderedDict([('Category', 'Construction'), ('Type', 'House'), ('Name', '')])
        self.animal = OrderedDict([('Category', 'Animal'), ('Type', ''), ('Name', '')])
        # The order of this is list important for which value that is returned
        # in case of multiple values of "best match"
        self.test_list = [self.cat, self.cat2, self.animal, self.dog, self.mouse, self.house]

    def test_find_keyword_get_list_not_implemented(self):
        vocab = Vocabulary('VOCAB MOCK')
        with self.assertRaises(NotImplementedError):
            vocab.find_keyword('an item')

    def test_find_keyword_not_found(self):
        vocab = Vocabulary('VOCAB MOCK')
        vocab.get_list = mock.MagicMock(return_value=self.test_list)
        with self.assertRaises(IndexError):
            vocab.find_keyword('Horse')

    def test_find_keyword(self):
        vocab = Vocabulary('VOCAB MOCK')
        vocab.get_list = mock.MagicMock(return_value=self.test_list)
        self.assertEqual(vocab.find_keyword('dog'), self.dog)
        self.assertEqual(vocab.find_keyword('Animal'), self.animal)

    def test_search_keyword(self):
        vocab = Vocabulary('VOCAB MOCK')
        vocab.get_list = mock.MagicMock(return_value=self.test_list)
        self.assertEqual(vocab.search('dog'), [self.dog])
        self.assertEqual(vocab.search('Animal'), [self.cat,
                                                  self.cat2,
                                                  self.animal,
                                                  self.dog,
                                                  self.mouse])

    def test_no_duplicate_in_search(self):
        vocab = Vocabulary('VOCAB MOCK')
        vocab.get_list = mock.MagicMock(return_value=self.test_list)
        self.assertEqual(vocab.search('Cat'), [self.cat, self.cat2])

    def test_no_empty_dict_in_sort_output(self):
        vocabulary = Vocabulary('test_vocabulary', categories=['foo', 'bar'])
        entry = {'foo': 'a', 'bar': 'b'}
        vocabulary_list = [{'Revision': '2016-01-08 13:40:40'}, entry]
        self.assertListEqual(vocabulary.sort_list(vocabulary_list), [OrderedDict(entry)])

    def test_sort_list(self):
        vocabulary = Vocabulary('test_vocabulary', categories=['Category', 'Type', 'Name'])
        self.assertListEqual(
            vocabulary.sort_list(self.test_list),
            [
                OrderedDict([('Category', 'Animal'), ('Type', 'Cat'), ('Name', '')]),
                OrderedDict([('Category', 'Animal'), ('Type', 'Cat'), ('Name', 'The cat')]),
                OrderedDict([('Category', 'Animal'), ('Type', ''), ('Name', '')]),
                OrderedDict([('Category', 'Animal'), ('Type', 'Dog'), ('Name', '')]),
                OrderedDict([('Category', 'Animal'), ('Type', 'Mouse'), ('Name', '')]),
                OrderedDict([('Category', 'Construction'), ('Type', 'House'), ('Name', '')]),
            ])

    def test_sort_list_aliases(self):
        vocabulary = Vocabulary('test_vocabulary', categories={
            'Category': 'class',
            'Type': 'kind',
            'Name': ''
        })
        self.assertListEqual(
            vocabulary.sort_list(self.test_list),
            [
                OrderedDict([('class', 'Animal'), ('kind', 'Cat'), ('Name', '')]),
                OrderedDict([('class', 'Animal'), ('kind', 'Cat'), ('Name', 'The cat')]),
                OrderedDict([('class', 'Animal'), ('kind', ''), ('Name', '')]),
                OrderedDict([('class', 'Animal'), ('kind', 'Dog'), ('Name', '')]),
                OrderedDict([('class', 'Animal'), ('kind', 'Mouse'), ('Name', '')]),
                OrderedDict([('class', 'Construction'), ('kind', 'House'), ('Name', '')]),
            ])

    def test_fuzzy_search(self):
        """Test that we get results in the right order using fuzzy
        search
        """
        vocabulary = Vocabulary('test')
        with mock.patch.object(vocabulary, 'get_list') as mock_get_list:
            d1 = {'a': 'foo', 'b': 'bar'}
            d2 = {'a': 'baz', 'b': 'qux'}
            d3 = {'a': 'quz', 'b': 'quux'}
            mock_get_list.return_value = [d1, d2, d3]

            self.assertEqual(vocabulary._fuzzy_search('baz', min_score=10.), [d2, d1, d3])
            self.assertEqual(vocabulary._fuzzy_search('baz', min_score=30.), [d2, d1])
            self.assertEqual(vocabulary._fuzzy_search('baz', min_score=50.), [d2])

    def test_default_fuzzy_search(self):
        """Test that _fuzzy_search is called with the default parameters
        """
        vocabulary = Vocabulary('test')
        with mock.patch.object(vocabulary, '_fuzzy_search') as mock_fuzzy_search:
            vocabulary.fuzzy_search('foo')
        mock_fuzzy_search.assert_called_once_with('foo')


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
