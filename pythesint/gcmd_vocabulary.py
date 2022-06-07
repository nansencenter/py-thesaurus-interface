from __future__ import absolute_import

from collections import OrderedDict
import requests
import warnings

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
        rlines = [line for line in r.text.splitlines()]
        gcmd_list = []

        _read_revision(rlines[0], gcmd_list)

        categories = _get_categories(rlines)
        self._check_categories(categories)

        for line in rlines[2:]:
            _read_line(line, gcmd_list, categories)

        return gcmd_list


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


def _get_categories(lines):
    '''Get the categories from the lines read from the source'''
    return lines[1].split(',')[:-1]


def _read_line(line, gcmd_list, categories):
    ''' Converts line into dictionary values for elements in the categories
    appends the dictionary to gcmd_list
    '''
    gcmd_keywords = line.split('","')
    gcmd_keywords[0] = gcmd_keywords[0].strip('"')
    if gcmd_keywords[0] == 'NOT APPLICABLE':
        return
    # Remove last item (the ID is not needed)
    gcmd_keywords.pop(-1)
    # skip record if it is longer than the definition of categories
    if len(gcmd_keywords) > len(categories):
        return
    line_kw = OrderedDict()
    for i, key in enumerate(categories):
        if i < len(gcmd_keywords):
            # if the record is equal to definition of categories
            line_kw[key] = gcmd_keywords[i]
        else:
            # if the record is shorter than definition of categories: add empty string
            line_kw[key] = ""
    gcmd_list.append(line_kw)
