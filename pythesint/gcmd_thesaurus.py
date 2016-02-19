from __future__ import absolute_import

import os
import requests
import json
from copy import copy
from pkg_resources import resource_filename
from collections import OrderedDict

class Thesaurus(object):
    def find_keyword(self, item):
        ''' Return the dictionary containing the given item in the provided list.
        The function returns only the lowest level match, i.e., the
        dictionary where the subgroups of the matching group are empty or the only
        match, if there is just one.

        Examples:

        1) Searching "Active Remote Sensing" in the instruments list will return
            {
                'Category': 'Earth Remote Sensing Instruments',
                'Class': 'Active Remote Sensing',
                'Type': '',
                'Subtype': '',
                'Short_Name': '',
                'Long_Name': ''
            }

        2) Searching "ASAR" in the instruments list will return
            {
                'Category': 'Earth Remote Sensing Instruments',
                'Class': 'Active Remote Sensing',
                'Type': 'Imaging Radars',
                'Subtype': '',
                'Short_Name': 'ASAR',
                'Long_Name': 'Advanced Synthetic Aperature Radar'
            }

        3) Searching "surface_backwards_scattering_coefficient_of_radar_wave" will
        return

        DOCTESTS:

        '''
        matches = []
        matching_key = ''
        for d in self._read_list():
            for key in d.keys():
                if d[key].upper()==item.upper():
                    matches.append(d)
                    matching_key = key
        keys = matches[0].keys()
        kw_group_index = keys.index(matching_key)
        ii = range(kw_group_index+1, len(keys))
        if len(matches)==1:
            return matches[0]
        # OBS: This works for the gcmd keywords but makes no sense for the cf
        # standard names - therefore always search the cf standard names by
        # standard_name only..
        for m in matches:
            remaining = {}
            for i in ii:
                remaining[keys[i]] = m[keys[i]]
            if not any(val for val in remaining.itervalues()):
                return m


class ThesaurusJSON(Thesaurus):
    def json_filename(self):
        json_path = resource_filename('pythesint', 'json')
        return os.path.join(json_path, '%s_list.json' % self.name.lower())

    def _read_list(self):
        ''' Read list from JSON '''
        if not os.path.exists(self.json_filename()):
            self._update_list()
        return json.load(open(self.json_filename()))

    def _update_list(self):
        ''' Write thesaurus to a JSON '''
        print('Writing json file %s' % self.name)
        json_path = os.path.split(self.json_filename())[0]
        if not os.path.exists(json_path):
            os.makedirs(json_path)
        with open(json_filename(self.name), 'w') as out:
            json.dump(self._fetch_data(), out, indent=4)


class GCMDThesaurus(ThesaurusJSON):
    base_url = 'http://gcmdservices.gsfc.nasa.gov/kms/concepts/concept_scheme/'
    def __init__(self, name, categories, url):
        self.name = name
        self.categories = categories
        self.url = self.base_url + url

    def _fetch_data():
        ''' Return list of GCMD standard keywords at provided url
    
        Parameters
        ----------
        list_name : the GCMD list name (must be one of the items in the standard_lists
        dictionary) in which;
            url is the URL of the desired GCMD list of valid keywords
            keyword_groups is a list containing the grouping of the keywords, e.g.,
            ['Category', 'Short_Name', 'Long_Name'] - used for verification
        '''    
        response = requests.get(self.url)
        # Boolean to determine if line information in the response object should be
        # stored as keywords
        do_record = False
    
        gcmd_list = []
        for line in response.iter_lines():
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

thesauri = {
    GCMD_SCIENCE_KEYWORDS: GCMDThesaurus(GCMD_SCIENCE_KEYWORDS,
            ['Category', 'Topic', 'Term', 'Variable_Level_1',
            'Variable_Level_2', 'Variable_Level_3', 'Detailed_Variable'],
            'sciencekeywords?format=csv'),
    GCMD_DATA_CENTERS: GCMDThesaurus(GCMD_DATA_CENTERS,
            ['Bucket_Level0', 'Bucket_Level1', 'Bucket_Level2',
            'Bucket_Level3', 'Short_Name', 'Long_Name', 'Data_Center_URL'],
            'providers?format=csv'),
    GCMD_INSTRUMENTS: GCMDThesaurus(GCMD_INSTRUMENTS,
        ['Category', 'Class', 'Type', 'Subtype', 'Short_Name',
            'Long_Name'],
        'instruments?format=csv'),
    GCMD_PLATFORMS: GCMDThesaurus(GCMD_PLATFORMS,
        ['Category', 'Series_Entity', 'Short_Name', 'Long_Name'],
        'platforms?format=csv'),
    GCMD_LOCATIONS: GCMDThesaurus(GCMD_LOCATIONS,
        ['Location_Category', 'Location_Type',
        'Location_Subregion1', 'Location_Subregion2',
        'Location_Subregion3'],
        'locations?format=csv')
}


def get_instrument(item):
    return thesauri[GCMD_INSTRUMENTS].find_keyword(item)

def get_platform(item):
    return thesauri[GCMD_SCIENCE_KEYWORDS].find_keyword(item)
    
def get_science_keyword(item):
    return thesauri[GCMD_SCIENCE_KEYWORDS].find_keyword(item)
    
def get_data_center(item):
    return thesauri[GCMD_DATA_CENTERS].find_keyword(item)

def get_location(item):
    return thesauri[GCMD_LOCATIONS].find_keyword(item)
