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

    def test_get_gcmd_instruments_list(self):
       self.assertIsInstance(pti.get_gcmd_instruments(), list)

    def test_get_gcmd_instrument(self):
        item = 'MERIS'
        self.assertIsInstance(pti.get_keyword('gcmd_instruments', item), dict)
        self.assertIsInstance(pti.get_keyword(pti.GCMD_INSTRUMENTS, item), dict)
        self.assertIsInstance(pti.get_gcmd_instrument(item), dict)

    def test_remove_and_get_gcmd_instrument(self):
        if os.path.exists(resource_filename('pythesint', 'json')):
            shutil.rmtree(resource_filename('pythesint', 'json'))
        item = 'MERIS'
        self.assertIsInstance(pti.get_keyword('gcmd_instruments', item), dict)
        self.assertIsInstance(pti.get_keyword(pti.GCMD_INSTRUMENTS, item), dict)
        self.assertIsInstance(pti.get_gcmd_instrument(item), dict)

    def test_get_gcmd_platform(self):
        item = 'AQUA'
        self.assertIsInstance(pti.get_keyword('gcmd_platforms', item), dict)
        self.assertIsInstance(pti.get_keyword(pti.GCMD_PLATFORMS, item), dict)
        self.assertIsInstance(pti.get_gcmd_platform(item), dict)

    def test_get_gcmd_science_keyword(self):
        item = 'sigma naught'
        self.assertIsInstance(pti.get_keyword('gcmd_science_keywords', item), dict)
        self.assertIsInstance(pti.get_keyword(pti.GCMD_SCIENCE_KEYWORDS, item), dict)
        self.assertIsInstance(pti.get_gcmd_science_keyword(item), dict)

    def test_get_gcmd_data_center(self):
        item = 'NERSC'
        self.assertIsInstance(pti.get_keyword('gcmd_data_centers', item), dict)
        self.assertIsInstance(pti.get_keyword(pti.GCMD_DATA_CENTERS, item), dict)
        self.assertIsInstance(pti.get_gcmd_data_center(item), dict)

    def test_get_gcmd_location(self):
        item = 'europe'
        self.assertIsInstance(pti.get_keyword('gcmd_locations', item), dict)
        self.assertIsInstance(pti.get_keyword(pti.GCMD_LOCATIONS, item), dict)
        self.assertIsInstance(pti.get_gcmd_location(item), dict)
        self.assertEquals(pti.get_gcmd_location(item)['Location_Subregion1'],
                '')

    def test_get_cf_standard_name(self):
        item = 'surface_backwards_scattering_coefficient_of_radar_wave'
        self.assertIsInstance(pti.get_keyword('cf_standard_names', item), dict)
        self.assertIsInstance(pti.get_keyword(pti.CF_STANDARD_NAMES, item), dict)
        self.assertIsInstance(pti.get_cf_standard_name(item), dict)

    def test_get_wkv_variable(self):
        item = 'surface_backwards_doppler_frequency_shift_of_radar_wave_due_to_surface_velocity'
        self.assertIsInstance(pti.get_wkv_variable(item), dict)

    def test_get_wkv_latitude(self):
        item = 'latitude'
        self.assertIsInstance(pti.get_wkv_variable(item), dict)

    def test_get_iso19115_topic_category(self):
        item = 'Oceans'
        self.assertIsInstance(pti.get_keyword('iso19115_topic_categories', item), dict)
        self.assertIsInstance(pti.get_keyword(pti.ISO19115_TOPIC_CATEGORIES, item), dict)
        self.assertIsInstance(pti.get_iso19115_topic_category(item), dict)

    def test_get_vertical_resolution_range(self):
        item = 'Point Resolution'
        self.assertIsInstance(pti.get_gcmd_vertical_resolution_range(item),
                dict)

    def test_get_temporal_resolution_range(self):
        item = 'Weekly Climatology'
        self.assertIsInstance(pti.get_gcmd_temporal_resolution_range(item),
                dict)

    def test_get_horizontal_resolution_range(self):
        item = 'Point Resolution'
        self.assertIsInstance(pti.get_gcmd_horizontal_resolution_range(item),
                dict)

    def test_get_project(self):
        item = 'aeronet'
        self.assertIsInstance(pti.get_gcmd_project(item), dict)

    def test_get_url_content_type(self):
        item = 'kml'
        self.assertIsInstance(pti.get_gcmd_url_content_type(item), dict)

    def test_get_fake_instrument(self):
        item = 'FakeItem'
        self.assertRaises(IndexError, pti.get_gcmd_instrument, item)

    def test_update(self):
        pti.update_vocabulary('gcmd_instruments')
        pti.update_vocabulary('gcmd_platforms')
        pti.update_vocabulary('gcmd_science_keywords')
        pti.update_vocabulary('gcmd_data_centers')
        pti.update_vocabulary('gcmd_locations')
        pti.update_vocabulary('cf_standard_names')
        pti.update_vocabulary('iso19115_topic_categories')
        pti.update_wkv_variable()

if __name__ == "__main__":
    unittest.main()
