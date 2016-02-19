'''
pythesint.pythesint : Main module for the py-thesaurus-interface package
'''
from __future__ import absolute_import

from pythesint.gcmd_thesaurus import thesauri as gcmd_thesauri
from pythesint.cf_thesaurus import thesauri as cf_thesauri

thesauri = {}
thesauri.update(gcmd_thesauri)
thesauri.update(cf_thesauri)

def get_keyword(name, item):
    ''' Gets keyword from existing thesauri '''
    return thesauri[name].find_keyword(item)

