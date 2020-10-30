import xml
import requests
from collections import OrderedDict

from pythesint.json_vocabulary import JSONVocabulary

class MMDAccessConstraints(JSONVocabulary):
    def _fetch_online_data(self):
        try:
            r = requests.get(self.url)
        except requests.RequestException:
            print("Could not get the vocabulary file at '{}'".format(self.url))
            raise
        dom = xml.dom.minidom.parseString(r.text.encode('utf-8').strip())
        # should only contain the standard_name_table:
        node = dom.childNodes[0].getElementsByTagName('skos:Collection')[0]

        label = node.getElementsByTagName('skos:prefLabel')[0].childNodes[0].data
        definition = node.getElementsByTagName('skos:definition')[0].childNodes[0].data
        details = OrderedDict({
                'aboutCollection': node.getAttribute('rdf:about'),
                'prefLabelCollection': label,
                'definitionCollection': definition})
        
        mmd_list = [details]
        for cnode in node.getElementsByTagName('skos:member'):
            if type(cnode)==xml.dom.minidom.Element:
                concept = cnode.getElementsByTagName('skos:Concept')[0]
                label = concept.getElementsByTagName('skos:prefLabel')[0].childNodes[0].data.strip()
                definition = concept.getElementsByTagName('skos:definition')[0].childNodes[0].data.strip()
                access_constraint = OrderedDict({
                    'prefLabel': label,
                    'definition': definition
                })
                mmd_list.append(access_constraint)
        return mmd_list

class MMDActivityType(MMDAccessConstraints):
    pass

class MMDAreas(MMDAccessConstraints):
    pass

class MMDOperStatus(MMDAccessConstraints):
    pass

class MMDPlatformType(MMDAccessConstraints):
    pass

class MMDUseConstraintType(MMDAccessConstraints):
    pass
