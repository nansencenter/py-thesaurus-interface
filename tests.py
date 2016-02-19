from __future__ import absolute_import

import unittest
import os, json

import pythesint as pti

class PythesintTest(unittest.TestCase):

    def test_get_keyword_instrument(self):
        self.assertIsInstance(pti.get_keyword('gcmd_instruments', 'MERIS'), dict)
        self.assertIsInstance(pti.get_keyword(pti.GCMD_INSTRUMENTS, 'MERIS'), dict)
        self.assertIsInstance(pti.get_gcmd_instrument('MERIS'), dict)
        self.assertIsInstance(pti.gcmd_keywords.get_instrument('MERIS'), dict)

if __name__ == "__main__":
    unittest.main()
