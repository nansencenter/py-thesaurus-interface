from __future__ import absolute_import

from pythesint.gcmd_thesaurus import thesauri as gcmd_thesauri
from pythesint.cf_thesaurus import thesauri as cf_thesauri
from pythesint.iso19115_thesaurus import thesauri as iso19115_thesauri
from pythesint.wkv_thesaurus import thesauri as wkv_thesauri

thesauri = {}
thesauri.update(gcmd_thesauri)
thesauri.update(cf_thesauri)
thesauri.update(iso19115_thesauri)
thesauri.update(wkv_thesauri)

def get_list(name):
    ''' Get list of keywords from given thesaurus <name>
    '''
    return thesauri[name].get_list()

def get_keyword(name, item):
    ''' Get keyword <item> from given thesaurus <name> '''
    return thesauri[name].find_keyword(item)

def update_thesaurus(name):
    ''' Update thesaurus content '''
    thesauri[name].update()
