from __future__ import absolute_import

import os
import json

from pythesint.vocabulary import Vocabulary
from pythesint.pathsolver import DATA_HOME

class JSONVocabulary(Vocabulary):
    def json_filename(self):
        return os.path.join('pythesint', 'json', '%s_list.json' % self.name.lower())

    def get_list(self):
        ''' Read list from JSON '''
        if not os.path.exists(self.json_filename()):
            self.update()
        return self.sort_list(json.load(open(self.get_filepath())))

    def update(self):
        ''' Write vocabulary to a JSON file '''
        print('Downloading and writing json file for %s' % self.name)
        json_path = os.path.split(self.get_filepath())[0]
        print(json_path)
        if not os.path.exists(json_path):
            os.makedirs(json_path)
        with open(self.get_filepath(), 'w') as out:
            json.dump(self._fetch_online_data(), out, indent=4)

    def get_filepath(self):
        return DATA_HOME + os.sep + self.json_filename()
