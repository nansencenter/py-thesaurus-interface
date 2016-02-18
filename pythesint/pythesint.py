'''
pythesint.pythesint : Main module for the py-thesaurus-interface package
'''
from __future__ import absolute_import

import os, json
from collections import OrderedDict
from pkg_resources import resource_filename

from pythesint import iso_topic_category_list

json_path = resource_filename('pythesint', 'json')

# Note: The kw_groups are used in validating the keyword groups in each list
# every time the list is downloaded from the gcmd services
gcmd_base_url = 'http://gcmdservices.gsfc.nasa.gov/kms/concepts/concept_scheme/'
cf_url = 'http://cfconventions.org/Data/cf-standard-names/30/src/cf-standard-name-table.xml'
standard_lists = {
    'gcmd_science_keywords': {
        'kw_groups': ['Category', 'Topic', 'Term', 'Variable_Level_1',
            'Variable_Level_2', 'Variable_Level_3', 'Detailed_Variable'],
        'url': gcmd_base_url + 'sciencekeywords?format=csv'
    },
    'gcmd_data_centers': {
        'kw_groups': ['Bucket_Level0', 'Bucket_Level1', 'Bucket_Level2',
            'Bucket_Level3', 'Short_Name', 'Long_Name', 'Data_Center_URL'],
        'url': gcmd_base_url + 'providers?format=csv'
    },
    'gcmd_instruments': {
        'kw_groups': ['Category', 'Class', 'Type', 'Subtype', 'Short_Name',
            'Long_Name'],
        'url': gcmd_base_url + 'instruments?format=csv'
    },
    'gcmd_platforms': {
        'kw_groups': ['Category', 'Series_Entity', 'Short_Name',
            'Long_Name'],
        'url': gcmd_base_url + 'platforms?format=csv'
    },
    'gcmd_locations': {
        'kw_groups': ['Location_Category', 'Location_Type',
            'Location_Subregion1', 'Location_Subregion2',
            'Location_Subregion3'],
        'url': gcmd_base_url + 'locations?format=csv'
    },
    'cf_standard_names': {
        'kw_groups': ['standard_name', 'canonical_units', 'grib', 'amip',
            'description'],
        'url': cf_url
    },
}

def json_filename(list_name):
    return '%s.json' % list_name.lower()

def write_json(list_name, path=json_path):
    ''' Write the list <list_name> to a json file

    <list_name> can be, e.g.,

    1) 'cf_standard_names'
    2) 'gcmd_science_keywords'
    3) 'gcmd_data_centers'
    4) 'gcmd_instruments'
    5) 'gcmd_platforms'
    6) 'gcmd_locations'
    '''
    from pythesint.gcmd_keywords import gcmd_standard_list
    from pythesint.cf_standard_names import cf_standard_list
    # Add other options as elif...
    if list_name.split('_')[0].lower()=='gcmd':
        ll = gcmd_standard_list(list_name)
    elif list_name.split('_')[0].lower()=='cf':
        ll = cf_standard_list()
    else:
        raise StandardError('List was not found')
    if not os.path.exists(path):
        os.mkdir(path)
    with open(os.path.join(path, json_filename(list_name)), 'w') as out:
        json.dump(ll, out, indent=4)

def dicts_from_json(list_name, update=False):
    json_fn = os.path.join(json_path, json_filename(list_name))
    if not os.path.isfile(json_fn) or update:
        print('Updating json file')
        write_json(list_name)
    keyword_list = json.load(open(os.path.join(json_path,
        json_filename(list_name))))
    # Create list with ordered dictionaries
    new_kw_list = []
    for dd in keyword_list:
        if dd.keys()[0]=='Revision':
            new_kw_list.append(dd)
            continue
        new_dict = OrderedDict()
        for key in standard_lists[list_name.lower()]['kw_groups']:
            new_dict[key] = dd[key]
        new_kw_list.append(new_dict)
    return new_kw_list

def get_keywords(list, **kwargs):
    return dicts_from_json(list, **kwargs)

def get_list_item(list, item):
    ''' Return the dictionary containing the given item in the provided list of
    dictionaries. The function returns only the lowest level match, i.e., the
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
    for d in list:
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


def get_instrument(item, **kwargs):
    return get_list_item(get_keywords('gcmd_instruments', **kwargs), item)

def get_platform(item, **kwargs):
    return get_list_item(get_keywords('gcmd_platforms', **kwargs), item)

def get_iso_topic_category(kw):
    for keyword in iso_topic_category_list.keywords:
        if keyword.upper()==kw.upper():
            return keyword

def get_science_keyword(item, **kwargs):
    return get_list_item(get_keywords('gcmd_science_keywords', **kwargs), item)

def get_data_center(item, **kwargs):
    return get_list_item(get_keywords('gcmd_data_centers', **kwargs), item)

def get_location(name, **kwargs):
    return get_list_item(get_keywords('gcmd_locations', **kwargs), name)

def get_cf_standard_name(standard_name, **kwargs):
    return get_list_item(get_keywords('cf_standard_names', **kwargs),
            standard_name)
