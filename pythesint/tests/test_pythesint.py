from __future__ import absolute_import

import unittest
import os, json, shutil
from pkg_resources import resource_filename

import pythesint as pti
from mock.mock import MagicMock

class PythesintTest(unittest.TestCase):

    # Missing tests
    # def test_write_json
    # def test_write_json_to_path

    def test_get_list(self):
        self.assertIsInstance(pti.get_wkv_variable_list(), list)
        self.assertIsInstance(pti.get_gcmd_instrument_list(), list)
        self.assertIsInstance(pti.get_gcmd_science_keyword_list(), list)
        self.assertIsInstance(pti.get_gcmd_provider_list(), list)
        self.assertIsInstance(pti.get_gcmd_platform_list(), list)
        self.assertIsInstance(pti.get_gcmd_location_list(), list)
        self.assertIsInstance(pti.get_gcmd_horizontalresolutionrange_list(), list)
        self.assertIsInstance(pti.get_gcmd_verticalresolutionrange_list(), list)
        self.assertIsInstance(pti.get_gcmd_temporalresolutionrange_list(), list)
        self.assertIsInstance(pti.get_gcmd_project_list(), list)
        self.assertIsInstance(pti.get_gcmd_rucontenttype_list(), list)
        self.assertIsInstance(pti.get_cf_standard_name_list(), list)
        self.assertIsInstance(pti.get_iso19115_topic_category_list(), list)
#        self.assertIsInstance(pti.get__list(), list)

    def test_remove_and_get_gcmd_instrument(self):
        if os.path.exists(resource_filename('pythesint', 'json')):
            shutil.rmtree(resource_filename('pythesint', 'json'))
        item = 'MERIS'
        self.assertIsInstance(pti.get_gcmd_instrument(item), dict)

    def test_get_gcmd_instrument(self):
        item = 'MERIS'
        self.assertIsInstance(pti.get_gcmd_instrument(item), dict)

    def test_get_gcmd_science_keyword(self):
        item = 'sigma naught'
        self.assertIsInstance(pti.get_gcmd_science_keyword(item), dict)

    def test_get_gcmd_provider(self):
        item = 'NERSC'
        self.assertIsInstance(pti.get_gcmd_provider(item), dict)

    def test_get_gcmd_platform(self):
        item = 'AQUA'
        self.assertIsInstance(pti.get_gcmd_platform(item), dict)

    def test_get_gcmd_location(self):
        item = 'NORWEGIAN SEA'
        self.assertIsInstance(pti.get_gcmd_location(item), dict)

    def test_get_gcmd_horizontalresolutionrange(self):
        item = '< 1 meter'
        self.assertIsInstance(pti.get_gcmd_horizontalresolutionrange(item), dict)

    def test_get_gcmd_verticalresolutionrange(self):
        item = '< 1 meter'
        self.assertIsInstance(pti.get_gcmd_verticalresolutionrange(item), dict)

    def test_get_gcmd_temporalresolutionrange(self):
        item = 'Decadal'
        self.assertIsInstance(pti.get_gcmd_temporalresolutionrange(item), dict)

    def test_get_gcmd_project(self):
        item = 'IPCC'
        self.assertIsInstance(pti.get_gcmd_project(item), dict)

    def test_get_gcmd_rucontenttype(self):
        item = 'THREDDS DATA'
        self.assertIsInstance(pti.get_gcmd_rucontenttype(item), dict)

    def test_get_cf_standard_name(self):
        item = 'surface_backwards_scattering_coefficient_of_radar_wave'
        self.assertIsInstance(pti.get_cf_standard_name(item), dict)

    def test_get_wkv_variable(self):
        item = 'surface_backwards_doppler_frequency_shift_of_radar_wave_due_to_surface_velocity'
        self.assertIsInstance(pti.get_wkv_variable(item), dict)

    def test_get_wkv_latitude(self):
        item = 'latitude'
        self.assertIsInstance(pti.get_wkv_variable(item), dict)

    def test_get_iso19115_topic_category(self):
        item = 'Oceans'
        self.assertIsInstance(pti.get_iso19115_topic_category(item), dict)

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

    def test_update_all(self):
        orig_vocab = pti.pythesint.vocabularies
        pti.pythesint.vocabularies = {'1': MagicMock(),
                                      'anothervocab': MagicMock(),
                                      'thirdvocab': MagicMock(),
                                      'instruments': MagicMock(),
                                      'something': MagicMock()}
        pti.update_all_vocabularies()
        for _, mock in pti.pythesint.vocabularies.iteritems():
            mock.update.assert_called_once_with()
        pti.pythesint.vocabularies = orig_vocab

    def test_update_vocabulary_specific(self):
        orig_vocab = pti.pythesint.vocabularies
        pti.pythesint.vocabularies = {'1': MagicMock(),
                                      'anothervocab': MagicMock(),
                                      'thirdvocab': MagicMock(),
                                      'instruments': MagicMock(),
                                      'something': MagicMock()}
        pti.update_vocabulary('1')
        pti.update_vocabulary('thirdvocab')
        for key, mock in pti.pythesint.vocabularies.iteritems():
            if (key in ['1', 'thirdvocab']):
                mock.update.assert_called_once_with()
            else:
                mock.update.assert_not_called()
        pti.pythesint.vocabularies = orig_vocab

if __name__ == "__main__":
    unittest.main()
