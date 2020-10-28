from __future__ import absolute_import

import os
import requests, json
from urllib.parse import urlparse
from collections import OrderedDict

from pythesint.json_vocabulary import JSONVocabulary


class CFVocabulary(JSONVocabulary):
    def _fetch_online_data(self):
        # Note the version number... Would probably be better to make it always
        # take the last version..
        try:
            r = requests.get(self.url)
        except requests.RequestException:
            print("Could not get the vocabulary file at '{}'".format(self.url))
            raise

        mmisw_CF = json.loads(r.text.encode('utf-8').strip())

        cf_list = []
        for k,v in mmisw_CF.items():
            stdname = OrderedDict()
            stdname['standard_name'] = os.path.basename(urlparse(k).path)
            units = ''
            if 'http://mmisw.org/ont/cf/parameter/canonical_units' in v.keys():
                units = v['http://mmisw.org/ont/cf/parameter/canonical_units'][0]['value']
            else:
                units = 'No units.'
            stdname['canonical_units'] = units
            if 'http://www.w3.org/2004/02/skos/core#definition' in v.keys():
                definition = v['http://www.w3.org/2004/02/skos/core#definition'][0]['value']
            else:
                definition = 'No definition available.'
            stdname['definition'] = definition
            cf_list.append(stdname)
        return cf_list

