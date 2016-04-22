from collections import OrderedDict

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
                if keyword.upper() in d[key].upper():
                    matches.append(d)

        return matches

    def update(self):
        pass

    def sort_list(self, list):
        retlist = []
        for dd in list:
            line_kw = OrderedDict()
            for _, key in enumerate(self.categories):
                try:
                    line_kw[key] = dd[key]
                except:
                    line_kw = dd
            retlist.append(line_kw)
        return retlist

    def get_list(self):
        raise NotImplementedError

