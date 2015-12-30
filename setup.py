#-------------------------------------------------------------------------------
# Name:
# Purpose:      
#
# Author:       Morten Wergeland Hansen
# Modified:
#
# Created:
# Last modified:
# Copyright:    (c) NERSC
# License:      
#-------------------------------------------------------------------------------
import sys, shutil
from setuptools import setup, find_packages

readme_file = 'README.md'
try:
    long_description = open(readme_file).read()
except IOError:
    sys.stderr.write("[ERROR] Cannot find file specified as "
        "``long_description`` (%s)\n" % readme_file)
    sys.exit(1)

install_requires = []

NAME = 'nerscmetadata'

def run_setup():

    from nerscmetadata.gcmd_keywords import write_json
    write_json()

    setup(name=NAME,
        version=0.1beta,
        description='Metadata conventions for geospatial data at NERSC',
        long_description=long_description,
        zip_safe=False,
        author=('Morten W. Hansen', 'Anton Korosov', 'Aleksander Vines',),
        author_email='mortenh@nersc.no',
        url='#',
        download_url='#',
        packages = find_packages(),
        package_data = {NAME: ['json/*.json']},
        include_package_data=True,
        install_requires = install_requires,
        test_suite='runtests.runtests',
        classifiers = [
            'Development Status :: 0 - Beta',
            'Environment :: Web Environment',
            'Framework :: ',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: BSD License',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Topic :: Utilities'
        ],
    )
    shutil.rmtree('dist')
    shutil.rmtree('build')
    shutil.rmtree('nerscmetadata.egg-info')

run_setup()

