#-------------------------------------------------------------------------------
# Name:
# Purpose:
#
# Author:       Morten Wergeland Hansen
# Modified:
#
# Created:
# Last modified:
# Copyright:    (c) NERSC
# License:
#-------------------------------------------------------------------------------
import unittest
import os, json
from nerscmetadata import gcmd_keywords

class GetGCMDKeywordsTest(unittest.TestCase):

    def test_write_json(self):
        gcmd_keywords.write_json()
        dd = json.load(open(os.path.join(gcmd_keywords.json_path,
            gcmd_keywords.json_filename)))
        self.assertEqual(type(dd), dict)

    def test_find_instrument(self):
        gcmd_keywords.get_instrument('MODIS')

    def test_find_platform(self):
        gcmd_keywords.get_platform('AQUA')
