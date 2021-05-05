from __future__ import absolute_import

import xml.dom.minidom
import re
import requests
from collections import OrderedDict

import pythesint.utils as utils
from pythesint.json_vocabulary import JSONVocabulary

class MMDBaseVocabulary(JSONVocabulary):
    @staticmethod
    def get_subnode_data(node, subnode_name):
        """Get the data contained in a subnode. Return an empty string
        if the subnode does not contain any data.
        """
        try:
            return node.getElementsByTagName(subnode_name)[0].childNodes[0].data.strip()
        except IndexError:
            return ''

    def _fetch_online_data(self, version=None):
        if version:
            url = utils.set_github_version(self.url, version)
        else:
            url = self.url

        try:
            r = requests.get(url)
        except requests.RequestException:
            print("Could not get the vocabulary file at '{}'".format(self.url))
            raise
        dom = xml.dom.minidom.parseString(r.text.encode('utf-8').strip())
        # should only contain the standard_name_table:
        node = dom.childNodes[0].getElementsByTagName('skos:Collection')[0]

        label = self.get_subnode_data(node, 'skos:prefLabel')
        definition = self.get_subnode_data(node, 'skos:definition')
        details = OrderedDict([
            ('aboutCollection', node.getAttribute('rdf:about')),
            ('prefLabelCollection', label),
            ('definitionCollection', definition)])

        if version:
            details['version'] = version

        mmd_list = [details]
        for cnode in node.getElementsByTagName('skos:member'):
            # This does not work in python2.7 because type(detail)=instance
            #if type(cnode)==xml.dom.minidom.Element:
            try:
                concept = cnode.getElementsByTagName('skos:Concept')[0]
            except (AttributeError, IndexError):
                continue
            else:
                label = self.get_subnode_data(concept, 'skos:prefLabel')
                definition = self.get_subnode_data(concept, 'skos:definition')

                access_constraint = OrderedDict([
                    ('prefLabel', label),
                    ('definition', definition)
                ])
                mmd_list.append(access_constraint)
        return mmd_list

class MMDAccessConstraints(MMDBaseVocabulary):
    pass

class MMDActivityType(MMDBaseVocabulary):
    pass

class MMDAreas(MMDBaseVocabulary):
    pass

class MMDOperStatus(MMDBaseVocabulary):
    pass

class MMDPlatformType(MMDBaseVocabulary):
    pass

class MMDUseConstraintType(MMDBaseVocabulary):
    pass
