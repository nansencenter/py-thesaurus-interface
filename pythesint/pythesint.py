from __future__ import absolute_import

from pkg_resources import resource_string

import yaml

def update_all_vocabularies():
    ''' Update all vocabularies '''
    for name in vocabularies.keys():
        vocabularies[name].update()

def _process_config():
    ''' Load info about all vocabularies from config and add to module '''
    # http://stackoverflow.com/questions/1621350/dynamically-adding-functions-to-a-python-module
    # http://stackoverflow.com/questions/4821104/python-dynamic-instantiation-from-string-name-of-a-class-in-dynamically-imported

    # load config file
    config = yaml.load(resource_string(__name__, 'pythesintrc.yaml'))
    current_module = __import__(__name__)

    # add get_ and update_ functions
    for cnf in config:
        voc_module = __import__('pythesint.' + cnf['module'],
                                fromlist=[__name__])
        voc_class = getattr(voc_module, cnf['class'])
        vocabulary = voc_class(cnf['name'], **cnf['kwargs'])
        vocabularies[cnf['name']] = vocabulary

        setattr(current_module, 'get_'+cnf['name'], vocabulary.find_keyword)
        setattr(current_module,
                'get_'+cnf['name']+'_list',
                vocabulary.get_list)
        setattr(current_module,
                'search_'+cnf['name']+'_list',
                vocabulary.search)
        setattr(current_module, 'update_'+cnf['name'], vocabulary.update)

vocabularies = {}
_process_config()
