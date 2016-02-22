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

here = path.abspath(path.dirname(__file__))
readme_file = 'README.md'
install_requires = ['requests']
NAME = 'pythesint'

# Get the long description from the README file
with open(path.join(here, readme_file), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name=NAME,

    version='0.4.0',

    description='A Python interface to various metadata vocabularies',
    long_description=long_description,

    zip_safe=False,

    author=('Morten W. Hansen', 'Anton A. Korosov', 'Aleksander Vines',),

    author_email='morten.hansen@nersc.no',

    url='https://github.com/nansencenter/py-thesaurus-interface',

    download_url='https://github.com/nansencenter/py-thesaurus-interface/archive/v0.4.0.tar.gz',

    packages=find_packages(),

    package_data={NAME: ['json/*.json']},

    include_package_data=True,

    install_requires=install_requires,

    test_suite='tests',

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

