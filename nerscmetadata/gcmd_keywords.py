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
import numpy as np

json_path = resource_filename('nerscmetadata', 'json')
json_filename = 'gcmd_keywords.json'

def gcmd_standard_list(url, keyword_groups):
    ''' Return list of GCMD standard keywords at provided url

    Parameters
    ----------
    url : char
        The URL of the desired GCMD list of valid keywords
    keyword_groups: list
        A list containing the grouping of the keywords, e.g., ['Category',
        'Short_Name', 'Long_Name'] - used for verification
    '''

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
            if not gcmd_keywords[-2] and not gcmd_keywords[-1]:
                # Missing short_name and long_name, so no actual instrument..
                continue
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

def write_json(filename=json_filename, path=json_path):
    base_url = 'http://gcmdservices.gsfc.nasa.gov/kms/concepts/concept_scheme/'
    instruments_kw_groups = ['Category', 'Class', 'Type', 'Subtype',
            'Short_Name', 'Long_Name']
    instruments_url = base_url + 'instruments?format=csv'
    gcmd_instruments = gcmd_standard_list(instruments_url, instruments_kw_groups)

    platforms_kw_groups = ['Category', 'Series_Entity', 'Short_Name',
            'Long_Name']
    platforms_url = base_url + 'platforms?format=csv'
    gcmd_platforms = gcmd_standard_list(platforms_url, platforms_kw_groups)

    keywords = {
            'Instruments': gcmd_instruments, 
            'Platforms': gcmd_platforms,
        }
    if not os.path.exists(path):
        os.mkdir(path)
    with open(os.path.join(path, filename), 'w') as out:
        json.dump(keywords, out, indent=4)

def dict_from_json(update=False):
    json_fn = os.path.join(json_path, json_filename)
    if not os.path.isfile(json_fn) or update:
        print('Updating json file')
        write_json()
    return json.load(open(os.path.join(json_path, json_filename)))

def get_keywords(list, **kwargs):
    # Consider getting the keywords directly from a csv file instead of json
    return dict_from_json(**kwargs)[list]

def get_list_item(list, item):
    ''' Return the dictionary containing item in provided list of dictionaries '''
    indices = [('Short_Name' in d) and ( d['Short_Name']==item.upper() or
        d['Long_Name']==item.upper()) for d in list]
    d = np.where(indices)
    if len(d)>1 or len(d[0])>1:
        raise ValueError
    index = d[0][0]
    return list[index]

def get_instrument(short_or_long_name):
    return get_list_item(get_keywords('Instruments'), short_or_long_name)

def get_platform(short_or_long_name):
    return get_list_item(get_keywords('Platforms'), short_or_long_name)
