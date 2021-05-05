import unittest

import mock.mock as mock
import requests

from pythesint.wkv_vocabulary import WKVVocabulary


class WKVVocabularyTest(unittest.TestCase):
    def test_exception_on_unavailable_remote_file(self):
        voc = WKVVocabulary(name='test_voc', url='https://sdfghdfghd.nersc.no')
        with self.assertRaises(requests.RequestException):
            voc._fetch_online_data()

    def test_fetch_version(self):
        """Test that the specified version is fetched"""
        voc = WKVVocabulary(
            name='test_voc',
            url='https://raw.githubusercontent.com/nansencenter/nersc-vocabularies/master/nansat_wkv.yml')
        # We use the exception as side effect to skip the part of the
        # method we are not testing.
        # TODO: split _fetch_online_data() into several methods instead
        with mock.patch('requests.get') as mock_get:
            mock_get.return_value.text = '[]'
            self.assertListEqual(voc._fetch_online_data(), [])
            mock_get.assert_called_with(
                'https://raw.githubusercontent.com/nansencenter/nersc-vocabularies/master/'
                'nansat_wkv.yml')

            self.assertListEqual(voc._fetch_online_data(version=None), [])
            mock_get.assert_called_with(
                'https://raw.githubusercontent.com/nansencenter/nersc-vocabularies/master/'
                'nansat_wkv.yml')

            self.assertListEqual(voc._fetch_online_data(version=''), [])
            mock_get.assert_called_with(
                'https://raw.githubusercontent.com/nansencenter/nersc-vocabularies/master/'
                'nansat_wkv.yml')

            self.assertListEqual(
                voc._fetch_online_data(version='91912bb'),
                [{'version': '91912bb'}])
            mock_get.assert_called_with(
                'https://raw.githubusercontent.com/nansencenter/nersc-vocabularies/91912bb/'
                'nansat_wkv.yml')
