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
import os
import requests
import json
from copy import copy
from pkg_resources import resource_filename

from nerscmetadata import iso_topic_category_list

json_path = resource_filename('nerscmetadata', 'json')

base_url = 'http://gcmdservices.gsfc.nasa.gov/kms/concepts/concept_scheme/'
gcmd_lists = {
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
    'data_centers': {
        'kw_groups': ['Bucket_Level0', 'Bucket_Level1', 'Bucket_Level2',
            'Bucket_Level3', 'Short_Name', 'Long_Name', 'Data_Center_URL'],
        'url': base_url + 'providers?format=csv'
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
    url : char
        The URL of the desired GCMD list of valid keywords
    keyword_groups: list
        A list containing the grouping of the keywords, e.g., ['Category',
        'Short_Name', 'Long_Name'] - used for verification
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
            #if not gcmd_keywords[-2] and not gcmd_keywords[-1]:
            #    # Missing short_name and long_name, so no actual instrument..
            #    continue
            line_kw = {}
            for i, g in enumerate(kw_groups):
                line_kw[g] = gcmd_keywords[i]
            gcmd_list.append(line_kw)
        if line.split(',')[0].lower() == keyword_groups[0].lower():
            do_record = True
            kw_groups = line.split(',')
            kw_groups.pop(-1)
            # Make sure the group items are as expected
            assert kw_groups==keyword_groups
    return gcmd_list

def json_filename(list_name):
    return 'gcmd_%s_list.json' % list_name.lower()

def write_json(list_name, path=json_path):
    keywords = gcmd_standard_list(list_name)
    if not os.path.exists(path):
        os.mkdir(path)
    with open(os.path.join(path, json_filename(list_name)), 'w') as out:
        json.dump(keywords, out, indent=4)

def dicts_from_json(list_name, update=False):
    json_fn = os.path.join(json_path, json_filename(list_name))
    if not os.path.isfile(json_fn) or update:
        print('Updating json file')
        write_json(list_name)
    return json.load(open(os.path.join(json_path, json_filename(list_name))))

def get_keywords(list, **kwargs):
    return dicts_from_json(list, **kwargs)

def list_item_from_short_or_long_name(d, item):
    if (('Short_Name' in d and d['Short_Name'].upper()==item.upper()) or
            ( 'Long_Name' in d and  d['Long_Name'].upper()==item.upper())):
        return True
    else:
        return False

def list_item_from_group_name(d, item, group_name):
    if (group_name in d and d[group_name].upper()==item.upper()):
        return True
    else:
        return False

def get_list_item(list, item, kwgroup=None):
    ''' Return the dictionary containing item in provided list of dictionaries '''
    matches = []
    for d in list:
        if not kwgroup:
            if list_item_from_short_or_long_name(d, item):
                matches.append(d)
        else:
            if list_item_from_group_name(d, item, kwgroup):
                matches.append(d)

    if len(matches) > 1:
        raise ValueError('More than one keyword matching %s' % item)
    elif len(matches) == 0:
        raise ValueError('Cannot find %s' % item)

    return matches[0]

def get_instrument(short_or_long_name):
    return get_list_item(get_keywords('Instruments'), short_or_long_name)

def get_platform(short_or_long_name):
    return get_list_item(get_keywords('Platforms'), short_or_long_name)

def get_iso_topic_category(kw):
    for keyword in iso_topic_category_list.keywords:
        if keyword.upper()==kw.upper():
            return keyword

def get_data_center(short_or_long_name):
    return get_list_item(get_keywords('data_centers'), short_or_long_name)

def get_location(name):
    try:
        ll = get_list_item(get_keywords('locations'), name, 'Location_Subregion3')
    except ValueError:
        ll = None
    if not ll:
        try:
            ll = get_list_item(get_keywords('locations'), name, 'Location_Subregion2')
        except ValueError:
            ll = None
    if not ll:
        try:
            ll = get_list_item(get_keywords('locations'), name, 'Location_Subregion1')
        except ValueError:
            ll = None
    if not ll:
        try:
            ll = get_list_item(get_keywords('locations'), name, 'Location_Type')
        except ValueError:
            ll = None
    if not ll:
        try:
            ll = get_list_item(get_keywords('locations'), name, 'Location_Category')
        except ValueError:
            ll = None
    return ll

