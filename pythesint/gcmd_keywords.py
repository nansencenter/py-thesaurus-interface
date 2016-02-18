from __future__ import absolute_import

import os
import requests
import json
from copy import copy
from pkg_resources import resource_filename
from collections import OrderedDict

from pythesint import pythesint
from pythesint import iso_topic_category_list

json_path = resource_filename('pythesint', 'json')

base_url = 'http://gcmdservices.gsfc.nasa.gov/kms/concepts/concept_scheme/'
# Note: The kw_groups are used in validating the keyword groups in each list
# every time the list is downloaded from the gcmd services
gcmd_lists = {
    'science_keywords': {
        'kw_groups': ['Category', 'Topic', 'Term', 'Variable_Level_1',
            'Variable_Level_2', 'Variable_Level_3', 'Detailed_Variable'],
        'url': base_url + 'sciencekeywords?format=csv'
    },
    'data_centers': {
        'kw_groups': ['Bucket_Level0', 'Bucket_Level1', 'Bucket_Level2',
            'Bucket_Level3', 'Short_Name', 'Long_Name', 'Data_Center_URL'],
        'url': base_url + 'providers?format=csv'
    },
    'instruments': {
        'kw_groups': ['Category', 'Class', 'Type', 'Subtype', 'Short_Name',
            'Long_Name'],
        'url': base_url + 'instruments?format=csv'
    },
    'platforms': {
        'kw_groups': ['Category', 'Series_Entity', 'Short_Name',
            'Long_Name'],
        'url': base_url + 'platforms?format=csv'
    },
    'locations': {
        'kw_groups': ['Location_Category', 'Location_Type',
            'Location_Subregion1', 'Location_Subregion2',
            'Location_Subregion3'],
        'url': base_url + 'locations?format=csv'
    },
}

def gcmd_standard_list(list_name):
    ''' Return list of GCMD standard keywords at provided url

    Parameters
    ----------
    list_name : the GCMD list name (must be one of the items in the gcmd_lists
    dictionary) in which;
        url is the URL of the desired GCMD list of valid keywords
        keyword_groups is a list containing the grouping of the keywords, e.g.,
        ['Category', 'Short_Name', 'Long_Name'] - used for verification
    '''
    url = gcmd_lists[list_name.lower()]['url']
    keyword_groups = gcmd_lists[list_name.lower()]['kw_groups']

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

    ## Create list with ordered dictionaries
    #new_kw_list = []
    #for dd in keyword_list:
    #    if dd.keys()[0]=='Revision':
    #        new_kw_list.append(dd)
    #        continue
    #    new_dict = OrderedDict()
    #    for key in gcmd_lists[list_name.lower()]['kw_groups']:
    #        new_dict[key] = dd[key]
    #    new_kw_list.append(new_dict)

    return new_kw_list

    return gcmd_list

def get_instrument(item, **kwargs):
    return get_list_item(get_keywords('Instruments', **kwargs), item)

def get_platform(item, **kwargs):
    return get_list_item(get_keywords('Platforms', **kwargs), item)

def get_iso_topic_category(kw):
    for keyword in iso_topic_category_list.keywords:
        if keyword.upper()==kw.upper():
            return keyword

def get_science_keyword(item, **kwargs):
    return pythesint.get_list_item(get_keywords('science_keywords', **kwargs), item)

def get_data_center(item, **kwargs):
    return get_list_item(get_keywords('data_centers', **kwargs), item)

def get_location(name, **kwargs):
    return get_list_item(get_keywords('locations', **kwargs), name)
