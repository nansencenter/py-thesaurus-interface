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

json_path = resource_filename('nerscmetadata', 'json')
json_filename = 'gcmd_keywords.json'

def create_list_by_key(dict, key):
    if not dict.has_key(key):
        dict[key] = []

def create_dict_by_key(dict, key):
    if not dict.has_key(key):
        dict[key] = {}

def populate(keywords, dict, keyword_groups, post_kw=None):
    ''' Recursively populate dictionary (dict) with keys and values provided in
    the first argument (keywords)

    OBS: The method returns if the two last keywords are empty. Presently this
    works for the instruments and platforms lists. However, the Data Centers
    list (or providers) may require checking the last three keywords, and other
    lists may have other traits, so the method should be slightly updated if we
    also want these keywords...
    '''
    if post_kw is None:
        post_kw = []
    # If short_name and long_name are missing, we don't store anything..
    if not keywords[-2] and not keywords[-1]:
            return
    this_keyword = keywords.pop(0)
    this_kw_group = keyword_groups.pop(0)
    if not this_keyword:
        this_keyword = this_kw_group + '_MISSINGKEY'
    post_kw.append(this_keyword)
    if len(keywords)==2:
        create_list_by_key(dict, this_keyword)
        dict[this_keyword].append([keywords[0], keywords[1]])
        # Make sure list is removed from memory
        post_kw = None
    else:
        create_dict_by_key(dict, this_keyword)
        populate(keywords, dict[this_keyword], keyword_groups, post_kw)


def gcmd_standard_dict(url, keyword_groups, dict={}):
    ''' Create dictionary of GCMD standard keywords at provided url

    Parameters
    ----------
    url : char
        The URL of the desired GCMD list of valid keywords
    keyword_groups: list
        A list containing the grouping of the keywords, e.g., ['Category',
        'Short_Name', 'Long_Name']
    dict: dictionary
        The dictionary to populate
    '''

    # Get data from url
    response = requests.get(url)
    # Boolean to determine if line information in the response object should be
    # stored as keywords
    do_record = False
    
    for line in response.iter_lines():
        if 'Keyword Version' and 'Revision' in line:
            meta = line.split('","')
            dict['Revision'] = meta[1][10:]
        if do_record:
            gcmd_keywords = line.split('","')
            gcmd_keywords[0] = gcmd_keywords[0].strip('"')
            if gcmd_keywords[0] == 'NOT APPLICABLE':
                continue
            # Remove last item (the ID is not needed)
            gcmd_keywords.pop(-1) 
            # Create copy of the keyword list for recursive population of dict
            # in populate method
            kw_copy = copy(gcmd_keywords)
            kwg_copy = copy(keyword_groups)
            # Populate dictionary 
            if len(kw_copy)!=len(kwg_copy):
                continue
            populate(kw_copy, dict, kwg_copy)
        if line.split(',')[0].lower() == keyword_groups[0].lower():
            do_record = True
            kw_groups = line.split(',')
            kw_groups.pop(-1)
            # Make sure the group items are as expected
            assert kw_groups==keyword_groups

def write_json(filename=json_filename, path=json_path):
    base_url = 'http://gcmdservices.gsfc.nasa.gov/kms/concepts/concept_scheme/'
    keywords = {'Instruments': {}, 'Platforms': {}}
    instruments_kw_groups = ['Category', 'Class', 'Type', 'Subtype',
            'Short_Name', 'Long_Name']
    instruments_url = base_url + 'instruments?format=csv'
    gcmd_standard_dict(instruments_url, instruments_kw_groups,
            keywords['Instruments'])

    platforms_kw_groups = ['Category', 'Series_Entity', 'Short_Name',
            'Long_Name']
    platforms_url = base_url + 'platforms?format=csv'
    gcmd_standard_dict(platforms_url, platforms_kw_groups, keywords['Platforms'])
    with open(os.path.join(path, filename), 'w') as out:
        json.dump(keywords, out, indent=4)

def dict_from_json(update=False):
    json_fn = os.path.join(json_path, json_filename)
    if not os.path.isfile(json_fn) or update:
        print('Updating json file')
        write_json()
    return json.load(open(os.path.join(json_path, json_filename)))

def dict_depth(d, depth=0):
    if not isinstance(d, dict) or not d:
        return depth
    return max(dict_depth(v, depth+1) for k, v in d.iteritems())

def extract(dict_in, final, list_out=None):
    ''' Recursively get a list of keyword lists

    The returned list has a length equal to the depth of the dictionary
    (dict_in), and the last item, e.g., list_out[0][0][0][:] for depth=4, has
    the keyword list we're after. The list called final has "depth"=1 and is
    easier to work with...

    The code is a bit ugly and could probably be improved.. Alternatively, it
    would be much easier to just read directly from the csv-file...
    '''
    if not list_out:
        list_out = []
    if isinstance(dict_in, unicode):
        list_out=None
        return []
    if isinstance(dict_in, list):
        retval = []
        for item in dict_in:
            retval.append(copy(list_out) + item)
            final.append(copy(list_out) + item)
        list_out = None
        return retval
    return [extract(dict_in[k], final, copy(list_out) + [k]) for k, v in
            dict_in.iteritems()]

def lists_from_dict(dd):
    final = []
    ll = extract(dd, final)
    return final

def get_keywords(list, **kwargs):
    # Consider getting the keywords directly from a csv file instead of json
    dd = dict_from_json(**kwargs)[list]
    return lists_from_dict(dd)

