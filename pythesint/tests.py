from __future__ import absolute_import

import unittest
import os, json

class GetGCMDKeywordsTest(unittest.TestCase):

    def test_write_json(self):
        import pythesint
        for gcmd_list in pythesint.gcmd_keywords.gcmd_lists.keys():
            list_name = 'gcmd_'+gcmd_list
            pythesint.write_json(list_name)
            fn = os.path.join(pythesint.json_path,
                    pythesint.json_filename(list_name))
            dd = json.load(open(fn))
            self.assertIsInstance(dd, list)

        list_name = 'cf_standard_names'
        pythesint.write_json(list_name)
        fn = os.path.join(pythesint.json_path,
                    pythesint.json_filename(list_name))
        dd = json.load(open(fn))
        self.assertIsInstance(dd, list)

    def test_write_json_to_path(self):
        gcmd_list = 'gcmd_instruments'
        path = 'tmp/json_test'
        with self.assertRaises(OSError):
            pythesint.write_json(gcmd_list, path=path)
        path = 'json_test'
        pythesint.write_json(gcmd_list, path=path)
        fn = os.path.join(path,
                    pythesint.json_filename(gcmd_list))
        dd = json.load(open(fn))
        self.assertIsInstance(dd, list)
        os.unlink(fn)
        os.rmdir(path)

    def test_find_instrument(self):
        self.assertIsInstance(gcmd_keywords.get_instrument('MODIS'), dict)

    def test_rewrite_json_and_find_instrument(self):
        self.assertIsInstance(gcmd_keywords.get_instrument('MODIS',
            update=True), dict)

    def test_find_instrument_class(self):
        self.assertIsInstance(
                gcmd_keywords.get_instrument('active remote sensing'), 
                dict)

    def test_find_science_keyword_term(self):
        self.assertIsInstance(
                gcmd_keywords.get_science_keyword('curriculum support'), dict)

    def test_find_science_keyword(self):
        self.assertIsInstance(
                gcmd_keywords.get_science_keyword('sigma naught'), dict)

    def test_find_platform(self):
        self.assertIsInstance(gcmd_keywords.get_platform('AQUA'), dict)

    def test_find_iso_topic_category(self):
        self.assertIsInstance(gcmd_keywords.get_iso_topic_category('oceans'),
                str)

    def test_find_data_center(self):
        self.assertIsInstance(gcmd_keywords.get_data_center('NERSC'), dict)

    def test_find_location_category(self):
        self.assertIsInstance(gcmd_keywords.get_location('continent'), dict)

    def test_find_location_type(self):
        self.assertIsInstance(gcmd_keywords.get_location('africa'), dict)

    def test_find_location_subregion1(self):
        self.assertIsInstance(gcmd_keywords.get_location('central africa'), dict)

    def test_find_location_subregion2(self):
        self.assertIsInstance(gcmd_keywords.get_location('Angola'), dict)

    def test_find_location_subregion3(self):
        self.assertIsInstance(gcmd_keywords.get_location('HONG KONG'), dict)

