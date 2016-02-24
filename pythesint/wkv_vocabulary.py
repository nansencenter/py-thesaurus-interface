from __future__ import absolute_import

import yaml
import urllib2
from collections import OrderedDict

from pythesint.json_vocabulary import JSONVocabulary

WKV_VARIABLES = 'wkv_variables'

class WKVVocabulary(JSONVocabulary):
    base_url = 'http://gcmdservices.gsfc.nasa.gov/kms/concepts/concept_scheme/'
    name = WKV_VARIABLES

    def _fetch_online_data(self):
        ''' Return list of Well Known Variables from Nansat        '''
        response = urllib2.urlopen('https://raw.githubusercontent.com/nansencenter/nersc-vocabularies/master/nansat_wkv.yml')
        return yaml.load(response.read())

vocabularies = {
    WKV_VARIABLES: WKVVocabulary(),
}

def get_variable(item):
    return vocabularies[WKV_VARIABLES].find_keyword(item)
