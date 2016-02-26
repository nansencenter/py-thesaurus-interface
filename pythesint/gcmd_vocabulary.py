from __future__ import absolute_import

from collections import OrderedDict

from pythesint.json_vocabulary import JSONVocabulary, openURL


class GCMDVocabulary(JSONVocabulary):
    def _fetch_online_data(self):
        ''' Return list of GCMD standard keywords at provided url

        Parameters
        ----------
        list_name : the GCMD list name (must be one of the items in the standard_lists
        dictionary) in which;
            url is the URL of the desired GCMD list of valid keywords
            keyword_groups is a list containing the grouping of the keywords, e.g.,
            ['Category', 'Short_Name', 'Long_Name'] - used for verification
        '''
        response = openURL(self.url)
        gcmd_list = []
        for line in response.readlines():
            _read_line(line, gcmd_list, self.categories)

        return gcmd_list


def _read_line(line, gcmd_list, categories):
    if 'Keyword Version' and 'Revision' in line:
        meta = line.split('","')
        gcmd_list.append({'Revision': meta[1][10:]})
    elif line.split(',')[0].lower() == categories[0].lower():
        kw_groups = line.split(',')
        kw_groups.pop(-1)
        # Make sure the group items are as expected
        if kw_groups != categories:
            raise TypeError('%s is not equal to %s' %
                            (kw_groups, categories))
    else:
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
