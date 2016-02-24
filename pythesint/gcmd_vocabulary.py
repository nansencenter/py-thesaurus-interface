from __future__ import absolute_import

import urllib2
from collections import OrderedDict

from pythesint.json_vocabulary import  JSONVocabulary

class GCMDVocabulary(JSONVocabulary):

    base_url = 'http://gcmdservices.gsfc.nasa.gov/kms/concepts/concept_scheme/'

    def __init__(self, name, categories, url):
        self.name = name
        self.categories = categories
        self.url = self.base_url + url

    def _fetch_online_data(self):
        ''' Return list of GCMD standard keywords at provided url

        Parameters
        ----------
        list_name : the GCMD list name (must be one of the items in the standard_lists
        dictionary) in which;
            url is the URL of the desired GCMD list of valid keywords
            keyword_groups is a list containing the grouping of the keywords, e.g.,
            ['Category', 'Short_Name', 'Long_Name'] - used for verification
        '''
        response = urllib2.urlopen(self.url)
        # Boolean to determine if line information in the response object should be
        # stored as keywords
        do_record = False

        gcmd_list = []
        for line in response.readlines():
            if 'Keyword Version' and 'Revision' in line:
                meta = line.split('","')
                gcmd_list.append({'Revision': meta[1][10:]})
            if do_record:
                gcmd_keywords = line.split('","')
                gcmd_keywords[0] = gcmd_keywords[0].strip('"')
                if gcmd_keywords[0] == 'NOT APPLICABLE':
                    continue
                # Remove last item (the ID is not needed)
                gcmd_keywords.pop(-1)
                if len(gcmd_keywords)!=len(kw_groups):
                    continue
                line_kw = OrderedDict()
                for i, key in enumerate(kw_groups):
                    line_kw[key] = gcmd_keywords[i]
                gcmd_list.append(line_kw)
            if line.split(',')[0].lower() == self.categories[0].lower():
                do_record = True
                kw_groups = line.split(',')
                kw_groups.pop(-1)
                # Make sure the group items are as expected
                assert kw_groups==self.categories

        return gcmd_list

GCMD_INSTRUMENTS = 'gcmd_instruments'
GCMD_PLATFORMS = 'gcmd_platforms'
GCMD_SCIENCE_KEYWORDS = 'gcmd_science_keywords'
GCMD_DATA_CENTERS = 'gcmd_data_centers'
GCMD_LOCATIONS = 'gcmd_locations'

vocabularies = {
    GCMD_SCIENCE_KEYWORDS: GCMDVocabulary(GCMD_SCIENCE_KEYWORDS,
            ['Category', 'Topic', 'Term', 'Variable_Level_1',
            'Variable_Level_2', 'Variable_Level_3', 'Detailed_Variable'],
            'sciencekeywords?format=csv'),
    GCMD_DATA_CENTERS: GCMDVocabulary(GCMD_DATA_CENTERS,
            ['Bucket_Level0', 'Bucket_Level1', 'Bucket_Level2',
            'Bucket_Level3', 'Short_Name', 'Long_Name', 'Data_Center_URL'],
            'providers?format=csv'),
    GCMD_INSTRUMENTS: GCMDVocabulary(GCMD_INSTRUMENTS,
        ['Category', 'Class', 'Type', 'Subtype', 'Short_Name',
            'Long_Name'],
        'instruments?format=csv'),
    GCMD_PLATFORMS: GCMDVocabulary(GCMD_PLATFORMS,
        ['Category', 'Series_Entity', 'Short_Name', 'Long_Name'],
        'platforms?format=csv'),
    GCMD_LOCATIONS: GCMDVocabulary(GCMD_LOCATIONS,
        ['Location_Category', 'Location_Type',
        'Location_Subregion1', 'Location_Subregion2',
        'Location_Subregion3'],
        'locations?format=csv')
}

#def _get_list(name):
#    ''' Return list of standards <name>, e.g., instruments, platforms, etc.
#    '''
#    return vocabularies[name].get_list()

def _get_instruments():
    return vocabularies[GCMD_INSTRUMENTS].get_list()

def _get_instrument(item):
    return vocabularies[GCMD_INSTRUMENTS].find_keyword(item)

def _get_platform(item):
    return vocabularies[GCMD_PLATFORMS].find_keyword(item)

def _get_science_keyword(item):
    return vocabularies[GCMD_SCIENCE_KEYWORDS].find_keyword(item)

def _get_data_center(item):
    return vocabularies[GCMD_DATA_CENTERS].find_keyword(item)

def _get_location(item):
    return vocabularies[GCMD_LOCATIONS].find_keyword(item)

