'''
pythesint.pythesint : Main module for the py-thesaurus-interface package
'''
from __future__ import absolute_import

import os, json
from collections import OrderedDict
from pkg_resources import resource_filename

json_path = resource_filename('pythesint', 'json')

def read_json(list_name):
    return json.load(open(os.path.join(json_path, json_filename(list_name))))

def json_filename(list_name):
    return '%s_list.json' % list_name.lower()

def find_keyword_in_list(keyword_list, item):
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
    for d in keyword_list:
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

def update_json_file(list_name, new_keyword_list):
    ''' Write list with keywrod dicts into a json file '''
    json_fn = os.path.join(json_path, json_filename(list_name))
    print('Updating json file %s' % list_name)
    if not os.path.exists(path):
        os.mkdir(path)
    with open(os.path.join(path, json_filename(list_name)), 'w') as out:
        json.dump(new_keyword_list, out, indent=4)
