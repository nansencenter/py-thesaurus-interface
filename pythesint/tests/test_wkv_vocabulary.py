import unittest

import requests

from pythesint.wkv_vocabulary import WKVVocabulary


class WKVVocabularyTest(unittest.TestCase):
    def test_exception_on_unavailable_remote_file(self):
        voc = WKVVocabulary(name='test_voc', url='https://sdfghdfghd.nersc.no')
        with self.assertRaises(requests.RequestException):
            voc._fetch_online_data()
