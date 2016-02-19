from __future__ import absolute_import

import unittest
import os, json

import pythesint as pti

class PythesintTest(unittest.TestCase):

    def test_get_keyword_instrument(self):
        item = 'MERIS'
        self.assertIsInstance(pti.get_keyword('gcmd_instruments', item), dict)
        self.assertIsInstance(pti.get_keyword(pti.GCMD_INSTRUMENTS, item), dict)
        self.assertIsInstance(pti.get_gcmd_instrument(item), dict)
        self.assertIsInstance(pti.gcmd_keywords.get_instrument(item), dict)

    def test_get_keyword_platform(self):
        item = 'AQUA'
        self.assertIsInstance(pti.get_keyword('gcmd_platforms', item), dict)
        self.assertIsInstance(pti.get_keyword(pti.GCMD_PLATFORMS, item), dict)
        self.assertIsInstance(pti.get_gcmd_platform(item), dict)
        self.assertIsInstance(pti.gcmd_keywords.get_platform(item), dict)

if __name__ == "__main__":
    unittest.main()
