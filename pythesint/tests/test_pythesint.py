from __future__ import absolute_import
from __future__ import print_function

import requests
import collections
import unittest
import os
import shutil
from pkg_resources import resource_filename, resource_string

import pythesint as pti
from mock.mock import MagicMock, patch
from pythesint.pathsolver import DATA_HOME


class PythesintTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Delete stored json data to work with a clean slate
        shutil.rmtree(os.path.join(DATA_HOME, 'pythesint', 'json'))

    def test_update_all(self):
        pti.update_all_vocabularies()
        for _, vocab in pti.pythesint.vocabularies.items():
            self.assertIsInstance(vocab.get_list(), list)

    def test_get_list(self):
        # TODO - these should be generated from rc file!
        dicts = ['wkv_variable', 'gcmd_instrument', 'gcmd_science_keyword',
                 'gcmd_provider', 'gcmd_platform', 'gcmd_location',
                 'gcmd_horizontalresolutionrange',
                 'gcmd_verticalresolutionrange',
                 'gcmd_temporalresolutionrange', 'gcmd_project',
                 'gcmd_rucontenttype', 'cf_standard_name',
                 'iso19115_topic_category']
        for name in dicts:
            function = getattr(pti, 'get_' + name + '_list')
            self.assertIsInstance(function(), list)

    def test_remove_and_get_gcmd_instrument(self):
        if os.path.exists(resource_filename('pythesint', 'json')):
            shutil.rmtree(resource_filename('pythesint', 'json'))
        item = 'MERIS'
        self.assertIsInstance(pti.get_gcmd_instrument(item),
                collections.OrderedDict)

    def test_get_gcmd_instrument(self):
        item = 'MERIS'
        self.assertIsInstance(pti.get_gcmd_instrument(item),
                collections.OrderedDict)

    def test_search_gcmd_instrument_list(self):
        item = 'MERIS'
        self.assertIsInstance(pti.search_gcmd_instrument_list(item)[0],
                collections.OrderedDict)

    def test_get_gcmd_science_keyword(self):
        item = 'sigma naught'
        self.assertIsInstance(pti.get_gcmd_science_keyword(item),
                collections.OrderedDict)

    def test_get_gcmd_provider(self):
        item = 'NERSC'
        self.assertIsInstance(pti.get_gcmd_provider(item),
                collections.OrderedDict)

    def test_get_gcmd_platform(self):
        item = 'AQUA'
        self.assertIsInstance(pti.get_gcmd_platform(item),
                collections.OrderedDict)

    def test_get_gcmd_location(self):
        item = 'NORWEGIAN SEA'
        self.assertIsInstance(pti.get_gcmd_location(item),
                collections.OrderedDict)

    def test_get_gcmd_horizontalresolutionrange(self):
        item = '< 1 meter'
        self.assertIsInstance(pti.get_gcmd_horizontalresolutionrange(item),
                collections.OrderedDict)

    def test_get_gcmd_verticalresolutionrange(self):
        item = '< 1 meter'
        self.assertIsInstance(pti.get_gcmd_verticalresolutionrange(item),
                collections.OrderedDict)

    def test_get_gcmd_temporalresolutionrange(self):
        item = 'Decadal'
        self.assertIsInstance(pti.get_gcmd_temporalresolutionrange(item),
                collections.OrderedDict)

    def test_get_gcmd_project(self):
        item = 'IPCC'
        self.assertIsInstance(pti.get_gcmd_project(item),
                collections.OrderedDict)

    def test_get_gcmd_rucontenttype(self):
        item = 'THREDDS DATA'
        self.assertIsInstance(pti.get_gcmd_rucontenttype(item),
                collections.OrderedDict)

    def test_get_cf_standard_name(self):
        item = 'surface_backwards_scattering_coefficient_of_radar_wave'
        self.assertIsInstance(pti.get_cf_standard_name(item),
                collections.OrderedDict)

    def test_get_wkv_variable(self):
        item = 'surface_backwards_doppler_frequency_shift_of_radar_wave_due_to_surface_velocity'
        self.assertIsInstance(pti.get_wkv_variable(item),
                collections.OrderedDict)

    def test_get_wkv_latitude(self):
        item = 'latitude'
        self.assertIsInstance(pti.get_wkv_variable(item),
                collections.OrderedDict)

    def test_get_iso19115_topic_category(self):
        item = 'Oceans'
        self.assertIsInstance(pti.get_iso19115_topic_category(item),
                collections.OrderedDict)

    def test_get_fake_instrument(self):
        item = 'FakeItem'
        self.assertRaises(IndexError, pti.get_gcmd_instrument, item)

    def test_update_functions_exists(self):
        # TODO - these should be generated from rc file!
        functions = ['update_wkv_variable', 'update_gcmd_instrument',
                     'update_gcmd_science_keyword', 'update_gcmd_provider',
                     'update_gcmd_platform', 'update_gcmd_location',
                     'update_gcmd_horizontalresolutionrange',
                     'update_gcmd_verticalresolutionrange',
                     'update_gcmd_temporalresolutionrange',
                     'update_gcmd_project', 'update_gcmd_rucontenttype',
                     'update_cf_standard_name',
                     'update_iso19115_topic_category']
        for function in functions:
            self.assertTrue(hasattr(pti, function), 'Function is missing:%s' %
                            (function))

    def urls(self):
        # items() in general is inefficient on Python 2, but should be no problem with just a couple items.
        for key, voc in pti.pythesint.vocabularies.items():
            if hasattr(voc, 'url'):
                response = requests.get(voc.url)

    def test_update_all_mocked(self):
        orig_vocab = pti.pythesint.vocabularies
        pti.pythesint.vocabularies = {'1': MagicMock(),
                                      'anothervocab': MagicMock(),
                                      'thirdvocab': MagicMock(),
                                      'instruments': MagicMock(),
                                      'something': MagicMock()}
        pti.update_all_vocabularies()
        # items() in general is inefficient on Python 2, but should be no problem with just a couple items.
        for _, mock in pti.pythesint.vocabularies.items():
            mock.update.assert_called_once_with()
        pti.pythesint.vocabularies = orig_vocab

if __name__ == "__main__":
    unittest.main()
