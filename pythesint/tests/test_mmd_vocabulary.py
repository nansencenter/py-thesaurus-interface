import io
import unittest
import xml.dom.minidom
from collections import OrderedDict

import mock.mock as mock

from pythesint.mmd_vocabulary import MMDVocabulary

class MMDVocabularyTest(unittest.TestCase):

    base_file_contents = '''<?xml version="1.0"?>
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

    def setUp(self):
        self.voc = MMDVocabulary(name='test_voc', collection_label='Concept label')

    def test_get_subnode_data(self):
        """Test getting the data from a subnode"""
        dom = xml.dom.minidom.parseString(self.base_file_contents)
        collection = dom.childNodes[0].getElementsByTagName('skos:Collection')[0]
        self.assertEqual(
            self.voc.get_subnode_data(collection, 'skos:definition'),
            'Concept definition')

    def test_get_element_by_label(self):
        """Test getting the collection having a particular label"""
        dom = xml.dom.minidom.parseString(self.base_file_contents)
        self.assertEqual(
            self.voc.get_element_by_label(dom.documentElement, 'skos:Collection', 'Concept label'),
            dom.childNodes[0].getElementsByTagName('skos:Collection')[0])


    def test_fetch_online_data(self):
        """Test that right collection is extracted"""
        # We use the exception as side effect to skip the part of the
        # method we are not testing.
        # TODO: split _fetch_online_data() into several methods instead

        expected_list = [
            OrderedDict([
                ('aboutCollection', 'https://vocab.met.no/mmd/concept'),
                ('prefLabelCollection', 'Concept label'),
                ('definitionCollection', 'Concept definition')]),
            OrderedDict([
                ('prefLabel', 'Instance label'),
                ('definition', 'Instance definition')])
        ]

        with mock.patch.object(self.voc, '_download_data_file') as mock_download, \
                mock.patch('pythesint.mmd_vocabulary.open') as mock_open:
            # return a new buffer containing the desired contents
            # every time open is called
            mock_open.side_effect = lambda *a, **k: io.StringIO(self.base_file_contents)

            version = 'master'
            expected_list[0]['version'] = version
            # No version provided
            self.assertCountEqual(self.voc._fetch_online_data(), expected_list)
            mock_download.assert_called_with(version=version)

            self.assertCountEqual(self.voc._fetch_online_data(version=None), expected_list)
            mock_download.assert_called_with(version=version)

            self.assertCountEqual(self.voc._fetch_online_data(version=''), expected_list)
            mock_download.assert_called_with(version=version)

            # Version provided
            version = 'a5c8573'
            expected_list[0]['version'] = version
            self.assertCountEqual(self.voc._fetch_online_data(version=version), expected_list)
            mock_download.assert_called_with(version='a5c8573')


class DownloadTestCase(unittest.TestCase):
    """Tests for the MMDVocabulary._download_data_file() method"""

    def setUp(self):
        self.voc = MMDVocabulary(name='test_voc', collection_label='foo')
        self.mock_open = mock.patch('pythesint.mmd_vocabulary.open').start()
        self.mock_get = mock.patch('requests.get').start()
        self.addCleanup(mock.patch.stopall)

    def test_download_data_file_if_not_present(self):
        """The file should be downloaded if it is not already there"""
        with mock.patch('os.path.isfile', return_value=False):
            self.voc._download_data_file()

        self.mock_get.assert_called_with(self.voc.base_url, stream=True)

    def test_download_data_file_version(self):
        """Test that the specified version is downloaded"""
        with mock.patch('os.path.isfile', return_value=False):
            self.voc._download_data_file(version='v3.2')

        self.mock_get.assert_called_with(
            'https://raw.githubusercontent.com/metno/mmd/v3.2/thesauri/mmd-vocabulary.xml',
            stream=True)
