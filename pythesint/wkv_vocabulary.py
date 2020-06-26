from __future__ import absolute_import

import yaml
import requests

from pythesint.json_vocabulary import JSONVocabulary


class WKVVocabulary(JSONVocabulary):
    def _fetch_online_data(self):
        ''' Return list of Well Known Variables from Nansat        '''
        try:
            r = requests.get(self.url)
        except requests.RequestException:
            print("Could not get the vocabulary file at '{}'".format(self.url))
            raise
        return yaml.load(r.text)

