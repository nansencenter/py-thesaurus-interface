from __future__ import absolute_import

from xml.dom.minidom import parseString
import requests
from pythesint.json_vocabulary import JSONVocabulary


class CFVocabulary(JSONVocabulary):
    def _fetch_online_data(self, version=None):
        if version:
            params = {'version': version}
        else:
            params = {}

        try:
            r = requests.get(self.url, params=params)
        except requests.RequestException:
            print("Could not get the vocabulary file at '{}'".format(self.url))
            raise
        dom = parseString(r.text.encode('utf-8').strip())
        # should only contain the standard_name_table:
        node = dom.childNodes[0]

        details = {}
        metadata_details = node.getElementsByTagName('owl:Ontology')[0]
        for detail in metadata_details.childNodes:
            # This does not work in python2.7 because type(detail)=instance
            #if type(detail)==xml.dom.minidom.Element:
            try:
                details[detail.nodeName] = detail.childNodes[0].data
            except (AttributeError, IndexError):
                continue

        cf_list = [details]
        for cnode in node.getElementsByTagName('Standard_Name')[0].childNodes:
            #if type(cnode)==xml.dom.minidom.Element:
            try:
                entry = cnode.getElementsByTagName('Standard_Name')[0]
            except (AttributeError, IndexError):
                continue
            else:
                standard_name = entry.getAttribute('rdf:about')
                units = ''
                if entry.getElementsByTagName('canonical_units'):
                    units = entry.getElementsByTagName(
                        'canonical_units')[0].childNodes[0].nodeValue
                if entry.getElementsByTagName('skos:definition'):
                    definition = entry.getElementsByTagName(
                            'skos:definition')[0].childNodes[0].nodeValue
                stdname = {
                    'standard_name': standard_name,
                    'canonical_units': units,
                    'definition': definition
                }
                cf_list.append(stdname)
        return cf_list

