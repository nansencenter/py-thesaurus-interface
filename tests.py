from __future__ import absolute_import

import unittest
import os, json, shutil
from pkg_resources import resource_filename

import pythesint as pti

class PythesintTest(unittest.TestCase):

    # Missing tests
    #def test_write_json
    #def test_write_json_to_path

    def test_get_list(self):
        self.assertIsInstance(pti.get_list('gcmd_platforms'), list)
        self.assertIsInstance(pti.get_list(pti.GCMD_PLATFORMS), list)

    #def test_get_list_from_path

    def test_get_list_directly_from_gcmd_thesaurus(self):
       from pythesint import gcmd_thesaurus
       self.assertIsInstance(gcmd_thesaurus.get_list('Instruments'), list)

    def test_get_gcmd_instrument(self):
        item = 'MERIS'
        self.assertIsInstance(pti.get_keyword('gcmd_instruments', item), dict)
        self.assertIsInstance(pti.get_keyword(pti.GCMD_INSTRUMENTS, item), dict)
        self.assertIsInstance(pti.get_gcmd_instrument(item), dict)
        self.assertIsInstance(pti.gcmd_thesaurus.get_instrument(item), dict)

    def test_remove_and_get_gcmd_instrument(self):
        if os.path.exists(resource_filename('pythesint', 'json')):
            shutil.rmtree(resource_filename('pythesint', 'json'))
        item = 'MERIS'
        self.assertIsInstance(pti.get_keyword('gcmd_instruments', item), dict)
        self.assertIsInstance(pti.get_keyword(pti.GCMD_INSTRUMENTS, item), dict)
        self.assertIsInstance(pti.get_gcmd_instrument(item), dict)
        self.assertIsInstance(pti.gcmd_thesaurus.get_instrument(item), dict)

    def test_get_gcmd_platform(self):
        item = 'AQUA'
        self.assertIsInstance(pti.get_keyword('gcmd_platforms', item), dict)
        self.assertIsInstance(pti.get_keyword(pti.GCMD_PLATFORMS, item), dict)
        self.assertIsInstance(pti.get_gcmd_platform(item), dict)
        self.assertIsInstance(pti.gcmd_thesaurus.get_platform(item), dict)

    def test_get_gcmd_science_keyword(self):
        item = 'sigma naught'
        self.assertIsInstance(pti.get_keyword('gcmd_science_keywords', item), dict)
        self.assertIsInstance(pti.get_keyword(pti.GCMD_SCIENCE_KEYWORDS, item), dict)
        self.assertIsInstance(pti.get_gcmd_science_keyword(item), dict)
        self.assertIsInstance(pti.gcmd_thesaurus.get_science_keyword(item), dict)

    def test_get_gcmd_data_center(self):
        item = 'NERSC'
        self.assertIsInstance(pti.get_keyword('gcmd_data_centers', item), dict)
        self.assertIsInstance(pti.get_keyword(pti.GCMD_DATA_CENTERS, item), dict)
        self.assertIsInstance(pti.get_gcmd_data_center(item), dict)
        self.assertIsInstance(pti.gcmd_thesaurus.get_data_center(item), dict)

    def test_get_gcmd_location(self):
        item = 'europe'
        self.assertIsInstance(pti.get_keyword('gcmd_locations', item), dict)
        self.assertIsInstance(pti.get_keyword(pti.GCMD_LOCATIONS, item), dict)
        self.assertIsInstance(pti.get_gcmd_location(item), dict)
        self.assertIsInstance(pti.gcmd_thesaurus.get_location(item), dict)

    def test_get_cf_standard_name(self):
        item = 'surface_backwards_scattering_coefficient_of_radar_wave'
        self.assertIsInstance(pti.get_keyword('cf_standard_names', item), dict)
        self.assertIsInstance(pti.get_keyword(pti.CF_STANDARD_NAMES, item), dict)
        self.assertIsInstance(pti.get_cf_standard_name(item), dict)
        self.assertIsInstance(pti.cf_thesaurus.get_standard_name(item), dict)

    def test_get_wkv_variable(self):
        item = 'surface_backwards_doppler_frequency_shift_of_radar_wave_due_to_surface_velocity'
        self.assertIsInstance(pti.get_keyword('wkv_variables', item), dict)
        self.assertIsInstance(pti.get_keyword(pti.WKV_VARIABLES, item), dict)
        self.assertIsInstance(pti.get_wkv_variable(item), dict)
        self.assertIsInstance(pti.wkv_thesaurus.get_variable(item), dict)

    def test_get_iso19115_topic_category(self):
        item = 'Oceans'
        self.assertIsInstance(pti.get_keyword('iso19115_topic_categories', item), dict)
        self.assertIsInstance(pti.get_keyword(pti.ISO19115_TOPIC_CATEGORIES, item), dict)
        self.assertIsInstance(pti.get_iso19115_topic_category(item), dict)
        self.assertIsInstance(pti.iso19115_thesaurus.get_topic_category(item), dict)

    def test_get_fake_instrument(self):
        item = 'FakeItem'
        self.assertRaises(IndexError, pti.gcmd_thesaurus.get_instrument, item)

    def test_update(self):
        pti.update_thesaurus('gcmd_instruments')
        pti.update_thesaurus('gcmd_platforms')
        pti.update_thesaurus('gcmd_science_keywords')
        pti.update_thesaurus('gcmd_data_centers')
        pti.update_thesaurus('gcmd_locations')
        pti.update_thesaurus('cf_standard_names')
        pti.update_thesaurus('iso19115_topic_categories')

if __name__ == "__main__":
    unittest.main()
