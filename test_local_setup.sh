#!/bin/bash
SRC=$HOME/py/py-thesaurus-interface
ENV=$HOME/test_pythesint

echo 'Build dist'
cd $SRC
rm dist -rf
rm pythesint.egg-info -rf
rm build -rf
python setup.py sdist
echo
echo

echo 'Install dist'
cd $HOME
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
export PYTHONPATH=
rm  $ENV -rf
virtualenv $ENV
source $ENV/bin/activate
which pip
pip install $SRC/dist/*.tar.gz
python -c 'import pythesint as pti; print pti.get_gcmd_instrument("MERIS")'
deactivate

