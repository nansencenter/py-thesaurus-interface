from __future__ import absolute_import

import csv
import requests
import warnings
from collections import OrderedDict

from pythesint.json_vocabulary import JSONVocabulary


class GCMDVocabulary(JSONVocabulary):

    def _check_categories(self, categories):
        '''Print a warning if the categories are not the expected ones
        '''
        if set(self.categories) != set(categories):
            mismatch_categories = set(self.categories).difference(set(categories))
            warnings.warn(f'Unknown categories {mismatch_categories} in {self.name}')

    def _fetch_online_data(self, version=None):
        ''' Return list of GCMD standard keywords
            self.url must be set
        '''
        if version:
            params = {'version': version}
        else:
            params = {}

        try:
            r = requests.get(self.url, verify=False, params=params)
            r.raise_for_status()
        except requests.RequestException:
            print("Could not get the vocabulary file at '{}'".format(self.url))
            raise

        lines = r.text.splitlines()
        keywords = []
        # Add version+revision information
        self._read_revision(lines[0], keywords)
        # parse actual CSV contents
        reader = csv.DictReader(lines[1:], dialect='unix', restval='')
        self._check_categories(reader.fieldnames)
        keywords.extend(list(reader))
        # remove UUID and extra fields
        for kw in keywords[1:]:
            for key in ('UUID', None):
                try:
                    del kw[key]
                except KeyError:
                    pass

        return keywords

    @staticmethod
    def _read_revision(line, gcmd_list):
        ''' Reads the line, extracts the Revision into a new dictionary and appends
        it to gcmd_list
        '''
        # TODO: Cast exception if not found?
        if 'Keyword Version' and 'Revision' in line:
            meta = line.split('","')
            gcmd_list.append({
                'Revision': meta[1][10:],
                'Keyword Version': meta[0].split(': ')[1]
            })
