from __future__ import absolute_import

import os, urllib2, json
from xml.dom.minidom import parse, parseString
from pkg_resources import resource_filename

from pythesint.tools import (write_json,
                             read_json,
                             find_keyword_in_list,
                             json_filename)

def _read_list(list_name):
    if not os.path.exists(json_filename(list_name)):
        _update_list(list_name)

    return read_json(list_name)

def _update_list(list_name):
    new_keyword_list = _get_new_list(list_name)
    write_json(list_name, new_keyword_list)


CF_STANDARD_NAMES = 'cf_standard_names'
cf_url = 'http://cfconventions.org/Data/cf-standard-names/30/src/cf-standard-name-table.xml'
controller = {
    CF_STANDARD_NAMES: {
        'kw_groups': ['standard_name', 'canonical_units', 'grib', 'amip',
            'description'],
        'url': cf_url,
        'get_list' : _read_list,
        'update_list' : _update_list,
    },
}

'''
Note: this module has a lot of repetition from gcmd_keywords.py - it works but
we have to generalize the code and add tests
'''

def _get_new_list(list_name):
    # Note the version number... Would probably be better to make it always
    # take the last version..
    u1 = urllib2.urlopen(controller[list_name]['url'])
    dom = parse(u1)
    node = dom.childNodes[0] # should only contain the standard_name_table

    cf_list = []
    for entry in node.getElementsByTagName('entry'):
        standard_name = entry.attributes['id'].value
        units = ''
        if entry.getElementsByTagName(
                'canonical_units')[0].childNodes:
            units = entry.getElementsByTagName(
                'canonical_units')[0].childNodes[0].nodeValue
        grib = ''
        if entry.getElementsByTagName('grib')[0].childNodes:
            grib = entry.getElementsByTagName(
                'grib')[0].childNodes[0].nodeValue
        amip = ''
        if entry.getElementsByTagName('amip')[0].childNodes:
            amip = entry.getElementsByTagName(
                'amip')[0].childNodes[0].nodeValue
        desrc = ''
        if entry.getElementsByTagName('description')[0].childNodes:
            descr = entry.getElementsByTagName(
                'description')[0].childNodes[0].nodeValue
        stdname = {
                'standard_name': standard_name,
                'canonical_units': units,
                'grib': grib,
                'amip': amip,
                'description': descr
            }
        cf_list.append(stdname)
    return cf_list

def get_standard_name(item):
    return find_keyword_in_list(_read_list(CF_STANDARD_NAMES), item)
