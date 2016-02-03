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
        gcmd_list = 'instruments'
        gcmd_keywords.write_json(gcmd_list)
        fn = os.path.join(gcmd_keywords.json_path,
                gcmd_keywords.json_filename(gcmd_list))
        dd = json.load(open(fn))
        self.assertIsInstance(dd, list)

    def test_find_instrument(self):
        self.assertIsInstance(gcmd_keywords.get_instrument('MODIS'), dict)

    def test_find_platform(self):
        self.assertIsInstance(gcmd_keywords.get_platform('AQUA'), dict)

    def test_find_iso_topic_category(self):
        self.assertIsInstance(gcmd_keywords.get_iso_topic_category('oceans'),
                str)

    def test_find_data_center(self):
        self.assertIsInstance(gcmd_keywords.get_data_center('NERSC'), dict)

    def test_find_location_category(self):
        gcmd_keywords.get_continent('continent')

    def test_find_location_type(self):
        gcmd_keywords.get_location_type('africa')

    def test_find_location_subregion1(self):
        gcmd_keywords.get_location_type('central africa')

    def test_find_location_subregion2(self):
        gcmd_keywords.get_location_type('Angola')

    def test_find_location_subregion3(self):
        self.assertIsInstance(gcmd_keywords.get_location('HONG KONG'), dict)

