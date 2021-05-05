import unittest
from collections import OrderedDict

import mock.mock as mock
import requests

from pythesint.mmd_vocabulary import MMDBaseVocabulary

class MMDVocabularyTest(unittest.TestCase):
    def test_exception_on_unavailable_remote_file(self):
        voc = MMDBaseVocabulary(name='test_voc', url='https://sdfghdfghd.nersc.no')
        with self.assertRaises(requests.RequestException):
            voc._fetch_online_data()

    def test_fetch_version(self):
        """Test that the specified version is fetched"""
        voc = MMDBaseVocabulary(
            name='test_voc',
            url='https://raw.githubusercontent.com/metno/mmd/master/thesauri/mmd_operstatus.xml')
        # We use the exception as side effect to skip the part of the
        # method we are not testing.
        # TODO: split _fetch_online_data() into several methods instead

        remote_page = '''<?xml version="1.0"?>
            <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
                xmlns:skos="http://www.w3.org/2004/02/skos/core#"
                xmlns:isothes="http://purl.org/iso25964/skos-thes#">
            <skos:Collection rdf:about="https://vocab.met.no/mmd/concept">
                <rdf:type rdf:resource="http://purl.org/iso25964/skos-thes#ConceptGroup"/>
                <skos:inScheme rdf:resource="https://vocab.met.no/mmd"/>
                <skos:prefLabel xml:lang="en">Concept label</skos:prefLabel>
                <skos:definition xml:lang="en">Concept definition</skos:definition>
                <skos:member>
                <skos:Concept rdf:about="https://vocab.met.no/mmd/concept/instance">
                    <skos:prefLabel xml:lang="en">Instance label</skos:prefLabel>
                    <skos:definition xml:lang="en">Instance definition</skos:definition>
                </skos:Concept>
                </skos:member>
            </skos:Collection>
            </rdf:RDF>
        '''

        expected_list = [
            OrderedDict([
                ('aboutCollection', 'https://vocab.met.no/mmd/concept'),
                ('prefLabelCollection', 'Concept label'),
                ('definitionCollection', 'Concept definition')]),
            OrderedDict([
                ('prefLabel', 'Instance label'),
                ('definition', 'Instance definition')])
        ]

        with mock.patch('requests.get') as mock_get:
            # No version provided
            mock_get.return_value.text = remote_page
            self.assertListEqual(voc._fetch_online_data(), expected_list)
            mock_get.assert_called_with(
                'https://raw.githubusercontent.com/metno/mmd/master/thesauri/mmd_operstatus.xml')

            self.assertListEqual(voc._fetch_online_data(version=None), expected_list)
            mock_get.assert_called_with(
                'https://raw.githubusercontent.com/metno/mmd/master/thesauri/mmd_operstatus.xml')

            self.assertListEqual(voc._fetch_online_data(version=''), expected_list)
            mock_get.assert_called_with(
                'https://raw.githubusercontent.com/metno/mmd/master/thesauri/mmd_operstatus.xml')

            # Version provided
            version = 'a5c8573'
            expected_list[0]['version'] = version
            self.assertListEqual(voc._fetch_online_data(version=version), expected_list)
            mock_get.assert_called_with(
                'https://raw.githubusercontent.com/metno/mmd/a5c8573/thesauri/mmd_operstatus.xml')
