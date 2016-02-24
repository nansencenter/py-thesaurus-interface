from __future__ import absolute_import

from pythesint.gcmd_vocabulary import vocabularies as gcmd_vocabularies
from pythesint.cf_vocabulary import vocabularies as cf_vocabularies
from pythesint.iso19115_vocabulary import vocabularies as iso19115_vocabularies
from pythesint.wkv_vocabulary import vocabularies as wkv_vocabularies

vocabularies = {}
vocabularies.update(gcmd_vocabularies)
vocabularies.update(cf_vocabularies)
vocabularies.update(iso19115_vocabularies)
vocabularies.update(wkv_vocabularies)


def get_list(name):
    ''' Get list of keywords from given vocabulary <name>
    '''
    return vocabularies[name].get_list()

def get_keyword(name, item):
    ''' Get keyword <item> from given vocabulary <name> '''
    return vocabularies[name].find_keyword(item)

def update_vocabulary(name):
    ''' Update vocabulary content '''
    vocabularies[name].update()
