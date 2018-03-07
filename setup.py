#-------------------------------------------------------------------------------
# Name:     Python Thesaurus Interface
# Purpose:  Python interface to various metadata vocabularies
#
# Author:   Morten Wergeland Hansen, Anton A. Korosov, Aleksander Vines
# Modified: 07.03.2018
#
# Created:  07.12.2015
# Copyright:(c) NERSC
# License:  GPLv3
#-------------------------------------------------------------------------------
from setuptools import setup, find_packages
from setuptools.command.install_scripts import install_scripts
from os import path

readme_file = 'README.md'
NAME = 'pythesint'
REQS = ['PyYAML', 'requests', 'xdg<=1.0.7;platform_system!="Windows"']

here = path.abspath(path.dirname(path.realpath(__file__)))

# Get the long description from the README file
long_description = ''
if path.exists(path.join(here, readme_file)):
    long_description = open(path.join(here, readme_file)).read()

class update_vocabularies(install_scripts):
    def run(self):
        install_scripts.run(self)
        import pythesint as pti
        pti.update_all_vocabularies()

setup(
    name=NAME,

    version='1.4.5',

    description='A Python interface to various metadata vocabularies',
    long_description=long_description,

    zip_safe=False,

    author='Morten W. Hansen, Anton A. Korosov, Aleksander Vines',

    author_email='morten.hansen@nersc.no',

    url='https://github.com/nansencenter/py-thesaurus-interface',

    download_url='https://github.com/nansencenter/py-thesaurus-interface/archive/v1.4.5.tar.gz',

    packages=find_packages(),

    include_package_data=True,

    setup_requires=REQS,

    install_requires=REQS,

    test_suite='pythesint.tests',

    license='GPLv3',

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Plugins',
        'Environment :: Console',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Atmospheric Science',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Utilities',
    ],

    keywords='metadata standards thesaurus vocabulary',

    cmdclass = {'install_scripts': update_vocabularies}
)
