from __future__ import absolute_import

from pythesint.json_vocabulary import  Vocabulary

'''
This module contains the ISO Topic Category list as listed at
http://gcmd.gsfc.nasa.gov/add/difguide/iso_topic_category.html

It seem to not be (freely) available in the ISO 19115 - Geographic Information
Metadata (http://www.isotc211.org/) Topic Category Code List
'''

class ISO19115Vocabulary(Vocabulary):
    name = 'iso19115_topic_category'
    iso_topic_category_list_keywords = [
        'Farming',
        'Biota',
        'Boundaries',
        'Climatology/Meteorology/Atmosphere',
        'Economy',
        'Elevation',
        'Environment',
        'Geoscientific Information',
        'Health',
        'Imagery/Base Maps/Earth Cover',
        'Intelligence/Military',
        'Inland Waters',
        'Location',
        'Oceans',
        'Planning Cadastre',
        'Society',
        'Structure',
        'Transportation',
        'Utilities/Communications',
        ]

    def get_list(self):
        ''' Convert list of keywords into list of dicts '''
        return [{'iso_topic_category' : keyword} for keyword in
            self.iso_topic_category_list_keywords]

ISO19115_TOPIC_CATEGORIES = 'iso19115_topic_categories'

vocabularies = {
    ISO19115_TOPIC_CATEGORIES : ISO19115Vocabulary()
}

def _get_topic_category(item):
    return vocabularies[ISO19115_TOPIC_CATEGORIES].find_keyword(item)
