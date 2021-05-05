'''
Created on Feb 25, 2016

@author: alevin
'''
from __future__ import absolute_import

import unittest
import mock.mock as mock
try:
    from StringIO import StringIO  # python 2
    StringIO.__enter__ = lambda *args: args[0]
    StringIO.__exit__ = lambda *args: args[0]
except ImportError:
    from io import StringIO  # python 3


from pythesint.json_vocabulary import JSONVocabulary


class JSONVocabularyTest(unittest.TestCase):

    def setUp(self):
        patch_fetch = mock.patch.object(JSONVocabulary, '_fetch_online_data', return_value=[])
        self.mock_fetch = patch_fetch.start()
        self.addCleanup(patch_fetch.stop)

    def test_update_no_version(self):
        """no version is provided"""
        vocabulary = JSONVocabulary(name='test')
        # avoid writing to a real file
        with mock.patch('pythesint.json_vocabulary.open', return_value=StringIO()):
            vocabulary.update()
            vocabulary._fetch_online_data.assert_called_with(version=None)

    def test_update_with_version(self):
        """a version is provided as argument"""
        vocabulary = JSONVocabulary(name='test')
        # avoid writing to a real file
        with mock.patch('pythesint.json_vocabulary.open', return_value=StringIO()):
            vocabulary.update(version='9.1.5')
            vocabulary._fetch_online_data.assert_called_with(version='9.1.5')

    def test_update_version_in_config(self):
        """a version is provided in the configuration"""
        vocabulary = JSONVocabulary(name='test', version='9.1.4')
        # avoid writing to a real file
        with mock.patch('pythesint.json_vocabulary.open', return_value=StringIO()):
            vocabulary.update()
            vocabulary._fetch_online_data.assert_called_with(version='9.1.4')

    def test_update_override_config_version(self):
        """"""
        vocabulary = JSONVocabulary(name='test', version='9.1.4')
        # avoid writing to a real file
        with mock.patch('pythesint.json_vocabulary.open', return_value=StringIO()):
            vocabulary.update(version='9.1.5')
            vocabulary._fetch_online_data.assert_called_with(version='9.1.5')
