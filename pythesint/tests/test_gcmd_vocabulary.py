'''
Created on Feb 26, 2016

@author: alevin
'''
from __future__ import absolute_import

import unittest

import mock.mock as mock
import requests

import pythesint as pti
from pythesint.gcmd_vocabulary import GCMDVocabulary


class GCMDVocabularyTest(unittest.TestCase):

    def test_read_revision(self):
        gcmd_list = []
        line = ('"Keyword Version: 8.1","Revision: 2016-01-08 13:40:40","'
                'Timestamp: 2016-02-26 04:46:02","Terms Of Use: See '
                'http://gcmd.nasa.gov/r/l/TermsOfUse","The most up to date XML'
                ' representations can be found here: '
                'http://gcmd.earthdata.nasa.gov/kms/concepts/concept_scheme'
                '/instruments/?format=xml"')
        pti.gcmd_vocabulary.GCMDVocabulary._read_revision(line, gcmd_list)
        self.assertEqual(len(gcmd_list), 1)
        self.assertDictEqual(
            gcmd_list[0],
            {'Keyword Version': '8.1', 'Revision': '2016-01-08 13:40:40'})

    def test_get_location_by_type(self):
        type = 'africa'
        a = pti.get_gcmd_location(type)
        self.assertEqual(a['Location_Type'], 'AFRICA')

    def test_exception_on_unavailable_remote_file(self):
        voc = GCMDVocabulary(name='test_voc', url='https://sdfghdfghd.nersc.no')
        with self.assertRaises(requests.RequestException):
            voc._fetch_online_data()

    def test_fetch_version(self):
        """Test that the specified version is fetched"""
        voc = GCMDVocabulary(name='test_voc', url='https://sdfghdfghd.nersc.no')
        # We use the exception as side effect to skip the part of the
        # method we are not testing.
        # TODO: split _fetch_online_data() into several methods instead
        with mock.patch('requests.get', side_effect=requests.RequestException) as mock_get:
            with self.assertRaises(requests.RequestException):
                voc._fetch_online_data()
            mock_get.assert_called_with('https://sdfghdfghd.nersc.no', verify=False, params={})

            with self.assertRaises(requests.RequestException):
                voc._fetch_online_data(version=None)
            mock_get.assert_called_with('https://sdfghdfghd.nersc.no', verify=False, params={})

            with self.assertRaises(requests.RequestException):
                voc._fetch_online_data(version='')
            mock_get.assert_called_with('https://sdfghdfghd.nersc.no', verify=False, params={})

            with self.assertRaises(requests.RequestException):
                voc._fetch_online_data(version='9.1.5')
            mock_get.assert_called_with(
                'https://sdfghdfghd.nersc.no', verify=False, params={'version': '9.1.5'})

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
