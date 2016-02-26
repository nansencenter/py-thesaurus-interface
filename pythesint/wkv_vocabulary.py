from __future__ import absolute_import

import yaml

from pythesint.json_vocabulary import JSONVocabulary, openURL


class WKVVocabulary(JSONVocabulary):
    def _fetch_online_data(self):
        ''' Return list of Well Known Variables from Nansat        '''
        response = openURL(self.url)
        return yaml.load(response.read())

