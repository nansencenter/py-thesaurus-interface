from __future__ import absolute_import

import yaml
import requests

import pythesint.utils as utils
from pythesint.json_vocabulary import JSONVocabulary


class WKVVocabulary(JSONVocabulary):
    def _fetch_online_data(self, version=None):
        '''Return list of Well Known Variables from Nansat'''
        if version:
            url = utils.set_github_version(self.url, version)
        else:
            url = self.url

        try:
            r = requests.get(url)
        except requests.RequestException:
            print("Could not get the vocabulary file at '{}'".format(self.url))
            raise

        if version:
            wkv_list = [{'version': version}]
        else:
            wkv_list = []
        wkv_list.extend(yaml.safe_load(r.text))

        return wkv_list

