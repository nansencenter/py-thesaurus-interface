from __future__ import absolute_import

from collections import OrderedDict
import requests

from pythesint.json_vocabulary import JSONVocabulary


class GCMDVocabulary(JSONVocabulary):
    def _fetch_online_data(self):
        ''' Return list of GCMD standard keywords
            self.url and self.categories must be set
        '''
        r = requests.get(self.url, verify=False)
        rlines = [line for line in r.text.splitlines()]
        gcmd_list = []
        _read_revision(rlines[0], gcmd_list)
        _check_categories(rlines[1], self.categories)
        for line in rlines[2:]:
            _read_line(line, gcmd_list, self.categories)

        return gcmd_list


def _read_revision(line, gcmd_list):
    ''' Reads the line, extracts the Revision into a new dictionary and appends
    it to gcmd_list
    '''
    # TODO: Cast exception if not found?
    if 'Keyword Version' and 'Revision' in line:
        meta = line.split('","')
        gcmd_list.append({'Revision': meta[1][10:]})


def _check_categories(line, categories):
    ''' Throws an exception if the line does not match categories
    '''
    kw_groups = line.split(',')
    kw_groups.pop(-1)
    # Make sure the group items are as expected
    if kw_groups != categories:
        raise TypeError('%s is not equal to %s' % (kw_groups, categories))


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
    if len(gcmd_keywords) != len(categories):
        return
    line_kw = OrderedDict()
    for i, key in enumerate(categories):
        line_kw[key] = gcmd_keywords[i]
    gcmd_list.append(line_kw)
