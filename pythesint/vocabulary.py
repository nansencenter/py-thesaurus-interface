from collections import OrderedDict

from rapidfuzz.fuzz import token_set_ratio
from rapidfuzz.process import extract
from rapidfuzz.utils import default_process


class Vocabulary(object):
    def __init__(self, name, **kwargs):
        self.name = name
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def find_keyword(self, item):
        ''' Return the dictionary containing the given item in the provided list.
        The function returns only the lowest level match, i.e., the
        dictionary where the subgroups of the matching group are empty or the only
        match, if there is just one.

        Examples:

        1) Searching "Active Remote Sensing" in the instruments list will return
            {
                'Category': 'Earth Remote Sensing Instruments',
                'Class': 'Active Remote Sensing',
                'Type': '',
                'Subtype': '',
                'Short_Name': '',
                'Long_Name': ''
            }

        2) Searching "ASAR" in the instruments list will return
            {
                'Category': 'Earth Remote Sensing Instruments',
                'Class': 'Active Remote Sensing',
                'Type': 'Imaging Radars',
                'Subtype': '',
                'Short_Name': 'ASAR',
                'Long_Name': 'Advanced Synthetic Aperature Radar'
            }

        3) Searching "surface_backwards_scattering_coefficient_of_radar_wave" will
        return

        DOCTESTS:

        '''
        best_match = None
        best_match_empty_cells = 0
        for d in self.get_list():
            match = None
            match_empty_cells = 0
            for _, key in enumerate(d.keys()):
                if d[key].upper() == item.upper():
                    match = d
                # sum up number of empty cells after matched cell
                if match == d and len(d[key]) == 0:
                    match_empty_cells += 1
            # if match is found in this row, and
            #     if the best match is not found yet, or
            #     if the best match has less empty cells after matched cell
            # i.e., if we search for the word 'animal', then the dictionary
            # {'animal', ''} is a better match than {'animal', 'cat'}
            if (match is not None and
                (best_match is None or
                 match_empty_cells > best_match_empty_cells)):
                best_match = match
                best_match_empty_cells = match_empty_cells

        if best_match is None:
            raise IndexError('%s is not found in %s!' % (item, self.name))

        return best_match

    def search(self, keyword):
        ''' Search for keyword in a list and return all matches '''
        matches = []
        for d in self.get_list():
            for key in d.keys():
                if keyword.upper() in d[key].upper() and not d in matches:
                    matches.append(d)

        return matches

    def update(self, version=None):
        pass

    def sort_list(self, list):
        retlist = []
        for dd in list:
            line_kw = OrderedDict()
            has_aliases = isinstance(self.categories, dict)
            try:
                for key in self.categories:
                    if has_aliases:
                        # self.categories is a dict defining aliases
                        alias = self.categories.get(key)
                        # if an empty alias is defined, use the original category name
                        field_name = alias if alias else key
                    else:
                        # no alias is defined, just use the category name
                        field_name = key
                    line_kw[field_name] = dd[key]
            except KeyError:
                continue
            retlist.append(line_kw)
        return retlist

    def get_list(self):
        raise NotImplementedError

    def _fuzzy_search(self, search_string, scorer=token_set_ratio, processor=default_process,
                      results_limit=10, min_score=50.0):
        """Perform a fuzzy search on the vocabulary.
        Fully parameterized, meant to be called by self.fuzzy_search()
        """
        terms_list = self.get_list()
        choices = (' '.join(ordered_dict.values()).lower() for ordered_dict in terms_list)
        # returns a list of tuples (choice, similarity, index)
        # similarity is a float in [0.0, 100.0], 100.0 meaning the
        # search string is a subset of the choice string
        results = extract(search_string.lower(), choices,
                          scorer=scorer, processor=processor,
                          limit=results_limit, score_cutoff=min_score)

        return [terms_list[result[2]] for result in results]

    def fuzzy_search(self, search_string):
        """Perform a fuzzy search on the vocabulary terms.
        Uses default parameters, can be overriden in subclasses.
        The default scorer uses token set ratio, which gives the
        highest score when one of the strings is a subset of the other.
        Words order does not matter.
        """
        return self._fuzzy_search(search_string)
