'''
pythesint.pythesint : Main module for the py-thesaurus-interface package
'''
from __future__ import absolute_import
from pythesint.gcmd_keywords import gcmd_standard_list
from pythesint.cf_standard_names import cf_standard_list
from pkg_resources import resource_filename
json_path = resource_filename('pythesint', 'json')

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
    # Add other options as elif...
    if list_name.split('_')[0].lower()=='gcmd':
        ll = gcmd_standard_list('_'.join(list_name.split('_')[1:]))
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
    return json.load(open(os.path.join(json_path, json_filename(list_name))))

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
    for m in matches:
        remaining = {}
        for i in ii:
            remaining[keys[i]] = m[keys[i]]
        if not any(val for val in remaining.itervalues()):
            return m


