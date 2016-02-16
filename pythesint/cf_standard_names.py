import os, urllib2, json
from xml.dom.minidom import parse, parseString
from pkg_resources import resource_filename

''' 
Note: this module has a lot of repetition from gcmd_keywords.py - it works but
we have to generalize the code and add tests
'''

json_path = resource_filename('pythesint', 'json')

def json_filename():
    return 'cf_standard_names_list.json' 

def get_cf_list():
    # Note the version number... Would probably be better to make it always
    # take the last version..
    cf_url = 'http://cfconventions.org/Data/cf-standard-names/30/src/cf-standard-name-table.xml'
    u1 = urllib2.urlopen(cf_url)
    dom = parse(u1)
    node = dom.childNodes[0] # should only contain the standard_name_table
    
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
        desrc = ''
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

def write_json(path=json_path):
    cf_list = get_cf_list()
    if not os.path.exists(path):
        os.mkdir(path)
    with open(os.path.join(path, json_filename()), 'w') as out:
        json.dump(cf_list, out, indent=4)

def dicts_from_json(update=False):
    json_fn = os.path.join(json_path, json_filename())
    if not os.path.isfile(json_fn) or update:
        print('Updating json file')
        write_json()
    return json.load(open(os.path.join(json_path, json_filename())))
