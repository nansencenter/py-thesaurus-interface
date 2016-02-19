from __future__ import absolute_import

import os
import requests
import json
from copy import copy
from pkg_resources import resource_filename
from collections import OrderedDict

from pythesint.tools import update_json_file, read_json, find_keyword_in_list

def _update_list(list_name):
    new_keyword_list = _get_new_list(list_name)
    update_json_file(list_name, new_keyword_list)

GCMD_INSTRUMENTS = 'gcmd_instruments'
GCMD_PLATFORMS = 'gcmd_platforms'
GCMD_SCIENCE_KEYWORDS = 'gcmd_science_keywords'
GCMD_DATA_CENTERS = 'gcmd_data_centers'
GCMD_LOCATIONS = 'gcmd_locations'

gcmd_base_url = 'http://gcmdservices.gsfc.nasa.gov/kms/concepts/concept_scheme/'

controller = {
    GCMD_SCIENCE_KEYWORDS: {
        'kw_groups': ['Category', 'Topic', 'Term', 'Variable_Level_1',
            'Variable_Level_2', 'Variable_Level_3', 'Detailed_Variable'],
        'url': gcmd_base_url + 'sciencekeywords?format=csv',
        'get_list' : read_json,
        'update_list' : _update_list,
    },
    GCMD_DATA_CENTERS: {
        'kw_groups': ['Bucket_Level0', 'Bucket_Level1', 'Bucket_Level2',
            'Bucket_Level3', 'Short_Name', 'Long_Name', 'Data_Center_URL'],
        'url': gcmd_base_url + 'providers?format=csv',
        'get_list' : read_json,
        'update_list' : _update_list,
    },
    GCMD_INSTRUMENTS: {
        'kw_groups': ['Category', 'Class', 'Type', 'Subtype', 'Short_Name',
            'Long_Name'],
        'url': gcmd_base_url + 'instruments?format=csv',
        'get_list' : read_json,
        'update_list' : _update_list,
    },
    GCMD_PLATFORMS: {
        'kw_groups': ['Category', 'Series_Entity', 'Short_Name', 'Long_Name'],
        'url': gcmd_base_url + 'platforms?format=csv',
        'get_list' : read_json,
        'update_list' : _update_list,
    },
    GCMD_LOCATIONS: {
        'kw_groups': ['Location_Category', 'Location_Type',
            'Location_Subregion1', 'Location_Subregion2',
            'Location_Subregion3'],
        'url': gcmd_base_url + 'locations?format=csv',
        'get_list' : read_json,
        'update_list' : _update_list,
    },
}

def _get_new_list(list_name):
    ''' Return list of GCMD standard keywords at provided url

    Parameters
    ----------
    list_name : the GCMD list name (must be one of the items in the standard_lists
    dictionary) in which;
        url is the URL of the desired GCMD list of valid keywords
        keyword_groups is a list containing the grouping of the keywords, e.g.,
        ['Category', 'Short_Name', 'Long_Name'] - used for verification
    '''
    url = standard_lists[list_name.lower()]['url']
    keyword_groups = standard_lists[list_name.lower()]['kw_groups']

    # Get data from url
    response = requests.get(url)
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
        if line.split(',')[0].lower() == keyword_groups[0].lower():
            do_record = True
            kw_groups = line.split(',')
            kw_groups.pop(-1)
            # Make sure the group items are as expected
            assert kw_groups==keyword_groups
    return gcmd_list

def get_instrument(item):
    return find_keyword_in_list(read_json(GCMD_INSTRUMENTS), item)

def get_platform(item):
    return find_keyword_in_list(read_json(GCMD_PLATFORMS), item)

def get_science_keyword(item):
    return find_keyword_in_list(read_json(GCMD_SCIENCE_KEYWORDS), item)

def get_data_center(item):
    return find_keyword_in_list(read_json(GCMD_DATA_CENTERS), item)

def get_location(item):
    return find_keyword_in_list(read_json(GCMD_LOCATIONS), item)

def update_gcmd_lists():
    _update_list(GCMD_INSTRUMENTS)
    _update_list(GCMD_PLATFORMS)
    _update_list(GCMD_SCIENCE_KEYWORDS)
    _update_list(GCMD_DATA_CENTERS)
    _update_list(GCMD_LOCATIONS)

