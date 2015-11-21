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
        fn = 'gcmd_keywords.json'
        gcmd_keywords.write_json()
        dd = json.load(open(fn))
        os.remove(fn)
        self.assertEqual(type(dd), dict)
