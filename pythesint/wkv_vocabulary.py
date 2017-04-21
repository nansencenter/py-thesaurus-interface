from __future__ import absolute_import

import yaml
import requests

from pythesint.json_vocabulary import JSONVocabulary


class WKVVocabulary(JSONVocabulary):
    def _fetch_online_data(self):
        ''' Return list of Well Known Variables from Nansat        '''
        r = requests.get(self.url)
        return yaml.load(r.text)

