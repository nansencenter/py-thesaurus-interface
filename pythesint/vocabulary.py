class Vocabulary(object):

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
        matches = []
        matching_key = ''
        for d in self.get_list():
            for key in d.keys():
                if d[key].upper()==item.upper():
                    matches.append(d)
                    matching_key = key

        if len(matches) == 0:
            raise IndexError('%s is not found in %s!' % (item, self.name))

        keys = matches[0].keys()
        kw_group_index = keys.index(matching_key)
        ii = range(kw_group_index+1, len(keys))
        if len(matches)==1:
            return matches[0]
        # OBS: This works for the gcmd keywords but makes no sense for the cf
        # standard names - therefore always search the cf standard names by
        # standard_name only..
        for m in matches:
            remaining = {}
            for i in ii:
                remaining[keys[i]] = m[keys[i]]
            if not any(val for val in remaining.itervalues()):
                return m

    def update(self):
        pass

