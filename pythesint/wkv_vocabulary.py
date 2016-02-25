from __future__ import absolute_import

import urllib2

import yaml

from pythesint.json_vocabulary import JSONVocabulary

WKV_VARIABLES = 'wkv_variables'

class WKVVocabulary(JSONVocabulary):
    name = WKV_VARIABLES
    categories = ['standard_name', 'long_name', 'short_name', 'units', 'minmax', 'colormap']

    def _fetch_online_data(self):
        ''' Return list of Well Known Variables from Nansat        '''
        response = urllib2.urlopen('https://raw.githubusercontent.com/nansencenter/nersc-vocabularies/master/nansat_wkv.yml')
        return yaml.load(response.read())

vocabularies = {
    WKV_VARIABLES: WKVVocabulary(),
}

def get_variable(item):
    return vocabularies[WKV_VARIABLES].find_keyword(item)
