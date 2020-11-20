import unittest
import requests

from pythesint.mmd_vocabulary import MMDBaseVocabulary

class MMDVocabularyTest(unittest.TestCase):
    def test_exception_on_unavailable_remote_file(self):
        voc = MMDBaseVocabulary(name='test_voc', url='https://sdfghdfghd.nersc.no')
        with self.assertRaises(requests.RequestException):
            voc._fetch_online_data()

