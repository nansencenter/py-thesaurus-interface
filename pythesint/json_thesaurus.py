from __future__ import absolute_import

import os
import json
from pkg_resources import resource_filename

from pythesint.thesaurus import Thesaurus

class JSONThesaurus(Thesaurus):
    def json_filename(self):
        json_path = resource_filename('pythesint', 'json')
        return os.path.join(json_path, '%s_list.json' % self.name.lower())

    def _read_list(self):
        ''' Read list from JSON '''
        if not os.path.exists(self.json_filename()):
            self.update()
        return json.load(open(self.json_filename()))

    def update(self):
        ''' Write thesaurus to a JSON '''
        print('Downloading and writing json file for %s' % self.name)
        json_path = os.path.split(self.json_filename())[0]
        if not os.path.exists(json_path):
            os.makedirs(json_path)
        with open(self.json_filename(), 'w') as out:
            json.dump(self._fetch_data(), out, indent=4)
