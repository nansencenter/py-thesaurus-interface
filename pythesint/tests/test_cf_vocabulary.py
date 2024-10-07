import unittest

import mock.mock as mock
import requests

from pythesint.cf_vocabulary import CFVocabulary, ratio

class CFVocabularyTest(unittest.TestCase):
    def test_exception_on_unavailable_remote_file(self):
        voc = CFVocabulary(name='test_voc', url='https://sdfghdfghd.nersc.no')
        with self.assertRaises(requests.RequestException):
            voc._fetch_online_data()

    def test_fetch_version(self):
        """Test that the specified version is fetched"""
        voc = CFVocabulary(name='test_voc', url='https://sdfghdfghd.nersc.no')
        # We use the exception as side effect to skip the part of the
        # method we are not testing.
        # TODO: split _fetch_online_data() into several methods instead
        with mock.patch('requests.get', side_effect=requests.RequestException) as mock_get:
            with self.assertRaises(requests.RequestException):
                voc._fetch_online_data()
            mock_get.assert_called_with('https://sdfghdfghd.nersc.no', params={})

            with self.assertRaises(requests.RequestException):
                voc._fetch_online_data(version=None)
            mock_get.assert_called_with('https://sdfghdfghd.nersc.no', params={})

            with self.assertRaises(requests.RequestException):
                voc._fetch_online_data(version='')
            mock_get.assert_called_with('https://sdfghdfghd.nersc.no', params={})

            with self.assertRaises(requests.RequestException):
                voc._fetch_online_data(version='9.1.5')
            mock_get.assert_called_with(
                'https://sdfghdfghd.nersc.no', params={'version': '9.1.5'})

    def test_fuzzy_search(self):
        """Test that _fuzzy_search is called with the altered parameters
        """
        vocabulary = CFVocabulary('test')
        with mock.patch.object(vocabulary, '_fuzzy_search') as mock_fuzzy_search:
            vocabulary.fuzzy_search('foo')
        mock_fuzzy_search.assert_called_once_with(
            'foo', scorer=ratio, results_limit=10, min_score=90.0)
