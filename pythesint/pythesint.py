'''
pythesint.pythesint : Main module for the py-thesaurus-interface package
'''
from __future__ import absolute_import

import os, json
from collections import OrderedDict
from pkg_resources import resource_filename

from pythesint.tools import find_keyword_in_list
from pythesint.gcmd_keywords import controller as gcmd_controller
from pythesint.cf_keywords import controller as cf_controller

# collect information about all thesauri
controller = {}
controller.update(gcmd_controller)
controller.update(cf_controller)
#controller.update(iso_controller)

def get_keyword(list_name, item):
    ''' Gets keyword from existing lists '''
    get_list_func = controller[list_name]['get_list']

    return find_keyword_in_list(get_list_func(list_name), item)

def update_list(list_name):
    ''' Update local copy of the list with the newest release '''
    controller[list_name]['update_list'](list_name)

"""

from pythesint.gcmd_thesaurus import thesauri as gcmd_thesauri
thesauri = {}
thesauri.update(gcmd_thesauri)

def get_keyword(thes_name, item):
    ''' Gets keyword from existing thesauri '''
    # collect thesauri from gcmd, etc (as 'controller' above)
    return thesauri[thes_name].find_keyword(item)

"""
