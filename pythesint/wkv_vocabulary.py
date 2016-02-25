from __future__ import absolute_import

import urllib2

import yaml

from pythesint.json_vocabulary import JSONVocabulary

class WKVVocabulary(JSONVocabulary):
    def _fetch_online_data(self):
        ''' Return list of Well Known Variables from Nansat        '''
        response = urllib2.urlopen(self.url)
        return yaml.load(response.read())

