import unittest

import requests

from pythesint.cf_vocabulary import CFVocabulary


class CFVocabularyTest(unittest.TestCase):
    def test_exception_on_unavailable_remote_file(self):
        voc = CFVocabulary(name='test_voc', url='https://sdfghdfghd.nersc.no')
        with self.assertRaises(requests.RequestException):
            voc._fetch_online_data()
