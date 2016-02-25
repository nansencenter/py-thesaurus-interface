from __future__ import absolute_import

from os import path
from pkg_resources import resource_string

import yaml

from pythesint.cf_vocabulary import vocabularies as cf_vocabularies
from pythesint.iso19115_vocabulary import vocabularies as iso19115_vocabularies

vocabularies = {}
vocabularies.update(cf_vocabularies)
vocabularies.update(iso19115_vocabularies)

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

# http://stackoverflow.com/questions/1621350/dynamically-adding-functions-to-a-python-module
# http://stackoverflow.com/questions/4821104/python-dynamic-instantiation-from-string-name-of-a-class-in-dynamically-imported

## load config file
config = yaml.load(resource_string(__name__, 'pythesintrc.yaml'))
current_module = __import__(__name__)

# add get_ and update_ functions
for cnf in config:
    voc_module = __import__('pythesint.' + cnf['module'], fromlist=[__name__])
    voc_class = getattr(voc_module, cnf['class'])
    vocabulary = voc_class(cnf['name'], **cnf['kwargs'])

    setattr(current_module, 'get_'+cnf['name'], vocabulary.find_keyword)
    setattr(current_module, 'get_'+cnf['name']+'_list', vocabulary.get_list)
    setattr(current_module, 'update_'+cnf['name'], vocabulary.update)

