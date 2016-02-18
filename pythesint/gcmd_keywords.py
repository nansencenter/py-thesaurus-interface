from __future__ import absolute_import

import os
import requests
import json
from copy import copy
from pkg_resources import resource_filename
from collections import OrderedDict

from pythesint.pythesint import get_keywords
from pythesint.pythesint import get_list_item
from pythesint.pythesint import standard_lists

def gcmd_standard_list(list_name):
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

def get_instrument(item, **kwargs):
    from pythesint.pythesint import get_instrument
    return get_instrument(item, **kwargs)

def get_platform(item, **kwargs):
    from pythesint.pythesint import get_platform
    return get_platform(item, **kwargs)

def get_iso_topic_category(kw):
    from pythesint.pythesint import get_iso_topic_category
    return get_iso_topic_category(kw)

def get_science_keyword(item, **kwargs):
    from pythesint.pythesint import get_science_keyword
    return get_science_keyword(item, **kwargs)

def get_data_center(item, **kwargs):
    from pythesint.pythesint import get_data_center
    return get_data_center(item, **kwargs)

def get_location(name, **kwargs):
    from pythesint.pythesint import get_location
    return get_location(name, **kwargs)
