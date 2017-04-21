from __future__ import absolute_import

from xml.dom.minidom import parseString
import requests
from pythesint.json_vocabulary import JSONVocabulary


class CFVocabulary(JSONVocabulary):
    def _fetch_online_data(self):
        # Note the version number... Would probably be better to make it always
        # take the last version..
        r = requests.get(self.url)
        dom = parseString(r.text.encode('utf-8').strip())
        # should only contain the standard_name_table:
        node = dom.childNodes[0]

        cf_list = []
        for entry in node.getElementsByTagName('entry'):
            standard_name = entry.attributes['id'].value
            units = ''
            if entry.getElementsByTagName(
                    'canonical_units')[0].childNodes:
                units = entry.getElementsByTagName(
                    'canonical_units')[0].childNodes[0].nodeValue
            grib = ''
            if entry.getElementsByTagName('grib')[0].childNodes:
                grib = entry.getElementsByTagName(
                    'grib')[0].childNodes[0].nodeValue
            amip = ''
            if entry.getElementsByTagName('amip')[0].childNodes:
                amip = entry.getElementsByTagName(
                    'amip')[0].childNodes[0].nodeValue
            if entry.getElementsByTagName('description')[0].childNodes:
                descr = entry.getElementsByTagName(
                    'description')[0].childNodes[0].nodeValue
            stdname = {
                    'standard_name': standard_name,
                    'canonical_units': units,
                    'grib': grib,
                    'amip': amip,
                    'description': descr
                }
            cf_list.append(stdname)
        return cf_list

