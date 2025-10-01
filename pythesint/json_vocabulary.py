from __future__ import absolute_import

import os
import json

from pythesint.vocabulary import Vocabulary
from pythesint.pathsolver import DATA_HOME

class JSONVocabulary(Vocabulary):

    version_attributes = None

    def _fetch_online_data(self, version=None):
        raise NotImplementedError

    def get_relative_path(self):
        return os.path.join('pythesint', 'json', '%s_list.json' % self.name.lower())

    def _get_raw_list(self):
        '''Return list from JSON without any filtering'''
        if not os.path.exists(self.get_filepath()):
            self.update()
        with open(self.get_filepath(), 'r') as opened_file:
            return json.load(opened_file)

    def get_list(self):
        ''' Read list from JSON '''
        result = self._get_raw_list()
        return self.sort_list(result)

    def update(self, version=None):
        ''' Write vocabulary to a JSON file '''
        if not version:
            try:
                version = self.version
            except AttributeError:
                version = None
        print('Downloading and writing json file for %s' % self.name)
        json_path = os.path.split(self.get_filepath())[0]
        print(json_path)
        if not os.path.exists(json_path):
            os.makedirs(json_path)
        with open(self.get_filepath(), 'w') as out:
            json.dump(self._fetch_online_data(version=version), out, indent=4)

    def get_filepath(self):
        return os.path.join(DATA_HOME, self.get_relative_path())

    def get_version(self):
        if self.version_attributes:
            for kw in self._get_raw_list():
                if set(self.version_attributes).issubset(set(kw)):
                    return '-'.join(kw[v] for v in self.version_attributes)
        return None
