from __future__ import absolute_import

import yaml
import urllib2
from collections import OrderedDict

from pythesint.json_thesaurus import JSONThesaurus

WKV_VARIABLES = 'wkv_variables'

class WKVThesaurus(JSONThesaurus):
    base_url = 'http://gcmdservices.gsfc.nasa.gov/kms/concepts/concept_scheme/'
    name = WKV_VARIABLES
    def _fetch_data(self):
        ''' Return list of Well Known Variables from Nansat        '''
        response = urllib2.urlopen('https://raw.githubusercontent.com/nansencenter/nansat/wkvxml2wkvyml/nansat/wkv.yml')
        return yaml.load(response.read())

thesauri = {
    WKV_VARIABLES: WKVThesaurus(),
}

def get_variable(item):
    return thesauri[WKV_VARIABLES].find_keyword(item)
