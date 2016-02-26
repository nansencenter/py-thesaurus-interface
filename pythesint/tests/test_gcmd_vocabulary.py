'''
Created on Feb 26, 2016

@author: alevin
'''
from __future__ import absolute_import

import unittest
import pythesint as pti


class GCMDVocabularyTest(unittest.TestCase):

    def test_read_line_Revision(self):
        gcmd_list = []
        line = ('"Keyword Version: 8.1","Revision: 2016-01-08 13:40:40","'
                'Timestamp: 2016-02-26 04:46:02","Terms Of Use: See '
                'http://gcmd.nasa.gov/r/l/TermsOfUse","The most up to date XML'
                ' representations can be found here: '
                'http://gcmdservices.gsfc.nasa.gov/kms/concepts/concept_scheme'
                '/instruments/?format=xml"')
        pti.gcmd_vocabulary._read_revision(line, gcmd_list)
        self.assertEqual(len(gcmd_list), 1)
        self.assertDictEqual(gcmd_list[0], {'Revision': '2016-01-08 13:40:40'})

    def test_check_categories(self):
        line = ('Category,Class,Type,Subtype,Short_Name,Long_Name,UUID')
        categories = ['Category', 'Class', 'Type', 'Subtype', 'Short_Name',
                      'Long_Name']
        pti.gcmd_vocabulary._check_categories(line, categories)

    def test_check_categories_wrong(self):
        line = ('Category,Class,Type,Subtype,Short_Name,Long_Name,UUID')
        categories = ['Category', 'Type', 'Class', 'Subtype', 'Short_Name',
                      'Long_Name']
        with self.assertRaises(TypeError):
            pti.gcmd_vocabulary._check_categories(line, categories)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
