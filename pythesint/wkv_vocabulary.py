from __future__ import absolute_import

import urllib2
from xml.dom.minidom import parse

from pythesint.json_vocabulary import JSONVocabulary

WKV_VARIABLES = 'wkv_variables'

class WKVVocabulary(JSONVocabulary):
    base_url = 'http://gcmdservices.gsfc.nasa.gov/kms/concepts/concept_scheme/'
    name = WKV_VARIABLES
    categories = ['standard_name', 'long_name', 'short_name', 'units', 'minmax', 'colormap']

    def _fetch_online_data(self):
        ''' Return list of Well Known Variables from Nansat        '''
        wkv_xml = urllib2.urlopen('https://raw.githubusercontent.com/nansencenter/nersc-vocabularies/master/nansat_wkv.xml')
        wkv_dom = parse(wkv_xml)
        wkv_list = []

        for item in wkv_dom.getElementsByTagName('wkv'):
            wkv_dict = {}
            for cat in self.categories:
                wkv_dict[cat] = item.getElementsByTagName(cat)[0].childNodes[0].nodeValue
            wkv_list.append(wkv_dict)
        return wkv_list

vocabularies = {
    WKV_VARIABLES: WKVVocabulary(),
}

def get_variable(item):
    return vocabularies[WKV_VARIABLES].find_keyword(item)
