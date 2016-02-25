#!/bin/bash
SRC=$HOME/py/py-thesaurus-interface
ENV=$HOME/test_pythesint

echo 'Build dist'
cd $SRC
python setup.py sdist
echo
echo

echo 'Install dist'
cd $HOME
export PATH=/home/antonk/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/home/antonk/bin:/bin:/usr/local/java/jre1.7.0_60/bin:/opt/gdal/1.11.0/bin:/opt/hdf/4.2.10/bin:/opt/matlab/bin/:/home/antonk/bin
export PYTHONPATH=
rm  $ENV -rf
virtualenv $ENV
source $ENV/bin/activate
which pip
pip install $SRC/dist/pythesint-1.0.2.tar.gz
python -c 'import pythesint as pti; print pti.get_gcmd_instrument("MERIS")'
deactivate

