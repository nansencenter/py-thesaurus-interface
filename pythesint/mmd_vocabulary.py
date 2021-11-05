from __future__ import absolute_import

import hashlib
import json
import os
import os.path
import xml.dom.minidom
from collections import OrderedDict
from contextlib import closing

import requests

import pythesint.utils as utils
from pythesint.json_vocabulary import JSONVocabulary
from pythesint.pathsolver import DATA_HOME

class MMDVocabulary(JSONVocabulary):
    base_url = 'https://raw.githubusercontent.com/metno/mmd/master/thesauri/mmd-vocabulary.xml'
    base_file = os.path.join(DATA_HOME, 'pythesint', 'mmd-vocabulary.xml')

    @staticmethod
    def get_subnode_data(node, subnode_name):
        """Get the data contained in a subnode. Return an empty string
        if the subnode does not contain any data.
        """
        try:
            return node.getElementsByTagName(subnode_name)[0].childNodes[0].data.strip()
        except IndexError:
            return ''

    def get_element_by_label(self, parent, node_type, label):
        """Returns the collection which has the given label"""
        for node in parent.getElementsByTagName(node_type):
            if self.get_subnode_data(node, 'skos:prefLabel') == label:
                return node
        return None

    @staticmethod
    def _get_local_file_github_blob_sha(file_path):
        """Get the local file's blob SHA hash as used by github"""
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as f_h:
                contents = f_h.read()
            header_string = f"blob {len(contents)}\0"
            blob = bytes(header_string, encoding='utf-8') + contents
            return hashlib.sha1(blob).hexdigest()
        return None

    def _get_remote_file_github_blob_sha(self, version):
        """Get the remote file's blob sha hash from github"""
        endpoint = f"https://api.github.com/repos/metno/mmd/git/trees/{version}:thesauri"
        result = json.loads(requests.get(endpoint).text)
        for file_info in result['tree']:
            if file_info['path'] == 'mmd-vocabulary.xml':
                return file_info['sha']
        return None

    def _download_data_file(self, version=None):
        """Download the file containing all the vocabularies
        definitions if it is not already present
        """
        if version:
            url = utils.set_github_version(self.base_url, version)
        else:
            url = self.base_url

        # by comparing the hashes, we can check if we need to
        # download the file or not
        local_sha = self._get_local_file_github_blob_sha(self.base_file)
        remote_sha = self._get_remote_file_github_blob_sha(version)

        if (not os.path.isfile(self.base_file) or local_sha != remote_sha):
            with closing(requests.get(url, stream=True)) as response:
                with open(self.base_file, 'wb') as f_h:
                    f_h.write(response.content)

    def _fetch_online_data(self, version=None):
        """Download, if necessary, the file containing all the MMD
        vocabularies definitions. Then extract the requested collection
        and write it to a JSON file like any JSON vocabulary.
        """
        if not version:
            version = 'master'

        self._download_data_file(version=version)

        with open(self.base_file, 'r', encoding='utf-8') as f_h:
            dom = xml.dom.minidom.parse(f_h)

        document = dom.documentElement

        collection = self.get_element_by_label(document, 'skos:Collection', self.collection_label)

        if collection is None:
            raise ValueError(f"'{self.collection_label}' is not a valid collection label")

        definition = self.get_subnode_data(collection, 'skos:definition')
        details = OrderedDict([
            ('aboutCollection', collection.getAttribute('rdf:about')),
            ('prefLabelCollection', self.collection_label),
            ('definitionCollection', definition)])

        if version:
            details['version'] = version

        mmd_list = [details]
        for cnode in collection.getElementsByTagName('skos:member'):
            try:
                # some concepts are directly defined in the collection
                # members...
                concept = cnode.getElementsByTagName('skos:Concept')[0]
            except (AttributeError, IndexError):
                # ...while others are defined outside of the collection
                # and need to be retrieved using their resource URL
                resource_name = cnode.getAttribute('rdf:resource')

                concept = None
                for concept_element in document.getElementsByTagName('skos:Concept'):
                    if concept_element.getAttribute('rdf:about') == resource_name:
                        concept = concept_element
                        break

                if not concept:
                    continue

            label = self.get_subnode_data(concept, 'skos:prefLabel')
            definition = self.get_subnode_data(concept, 'skos:definition')
            access_constraint = OrderedDict([
                ('prefLabel', label),
                ('definition', definition)
            ])
            mmd_list.append(access_constraint)

        return mmd_list
