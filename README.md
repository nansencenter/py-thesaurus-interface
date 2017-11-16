[![Build Status](https://travis-ci.org/nansencenter/py-thesaurus-interface.svg?branch=master)](https://travis-ci.org/nansencenter/py-thesaurus-interface)
[![Coverage Status](https://coveralls.io/repos/github/nansencenter/py-thesaurus-interface/badge.svg?branch=master)](https://coveralls.io/github/nansencenter/py-thesaurus-interface?branch=master)

## py-thesaurus-interface
An interface to metadata vocabularies for geospatial and other geophysical data

## Install
```
pip install https://github.com/nansencenter/py-thesaurus-interface/archive/master.tar.gz
```
## Usage
```
import pythesint as pti
pti.get_gcmd_instrument('MERIS')
pti.get_gcmd_platform('ENVISAT')
pti.get_gcmd_provider('NERSC')
```

## Standards

The package follows the standards defined at NASA's Global Change Master Directory (GCMD) (http://gcmd.gsfc.nasa.gov) and the NetCDF-CF conventions (http://cfconventions.org/), plus possibly others that will be added as needs emerge... The standards are mapped in Python dictionaries and saved to json-files.

## Directory Interchange Format (DIF)

The DIF format is a descriptive and standardized format for exchanging information about scientific data sets. The py-thesaurus-interface package provides an interface to the keywords and formats defined at GCMD.

See: Directory Interchange Format (DIF) Writer's Guide, 2015. Global Change Master Directory. National Aeronautics and Space Administration. [http://gcmd.nasa.gov/add/difguide/].

## Controlled keyword vocabularies from GCMD

See: Global Change Master Directory (GCMD). 2015. GCMD Keywords, Version 8.1. Greenbelt, MD: Global Change Data Center, Science and Exploration Directorate, Goddard Space Flight Center (GSFC) National Aeronautics and Space Administration (NASA). URL:http://gcmd.nasa.gov/learn/keywords.html

