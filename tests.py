from __future__ import absolute_import

import unittest
import os, json

import pythesint as pti

class PythesintTest(unittest.TestCase):

    def test_get_gcmd_instrument(self):
        item = 'MERIS'
        self.assertIsInstance(pti.get_keyword('gcmd_instruments', item), dict)
        self.assertIsInstance(pti.get_keyword(pti.GCMD_INSTRUMENTS, item), dict)
        self.assertIsInstance(pti.get_gcmd_instrument(item), dict)
        self.assertIsInstance(pti.gcmd_keywords.get_instrument(item), dict)

    def test_get_gcmd_platform(self):
        item = 'AQUA'
        self.assertIsInstance(pti.get_keyword('gcmd_platforms', item), dict)
        self.assertIsInstance(pti.get_keyword(pti.GCMD_PLATFORMS, item), dict)
        self.assertIsInstance(pti.get_gcmd_platform(item), dict)
        self.assertIsInstance(pti.gcmd_keywords.get_platform(item), dict)

    def test_get_cf_standard_name(self):
        item = 'surface_backwards_scattering_coefficient_of_radar_wave'
        self.assertIsInstance(pti.get_keyword('cf_standard_names', item), dict)
        self.assertIsInstance(pti.get_keyword(pti.CF_STANDARD_NAMES, item), dict)
        self.assertIsInstance(pti.get_cf_standard_name(item), dict)
        self.assertIsInstance(pti.cf_keywords.get_standard_name(item), dict)

if __name__ == "__main__":
    unittest.main()
