# nersc-metadata
Metadata conventions for geospatial data at NERSC

This package is in early testing phase to solve the needs of https://github.com/nansencenter/nansat and https://github.com/nansencenter/nansen-cloud.

# Install
```sh
pip install pip install https://github.com/nansencenter/nersc-metadata/archive/master.tar.gz
```

# Standards

The package will follow standards defined at NASA's Global Change Master Directory (GCMD) (http://gcmd.gsfc.nasa.gov) and the NetCDF-CF conventions (http://cfconventions.org/), plus possibly others that will be added as needs emerge... The standards are added to Python dictionaries and may be saved to json-files.

## Directory Interchange Format (DIF) 

The DIF format is a descriptive and standardized format for exchanging information about scientific data sets. The nersc-metadata package will contain a validator to check that the format is followed, however with more strict requirements compared to http://gcmd.nasa.gov/add/difguide/WRITEADIF.pdf.

See: Directory Interchange Format (DIF) Writer's Guide, 2015. Global Change Master Directory. National Aeronautics and Space Administration. [http://gcmd.nasa.gov/add/difguide/]. 

## Controlled keyword vocabularies from GCMD

See: Global Change Master Directory (GCMD). 2015. GCMD Keywords, Version 8.1. Greenbelt, MD: Global Change Data Center, Science and Exploration Directorate, Goddard Space Flight Center (GSFC) National Aeronautics and Space Administration (NASA). URL:http://gcmd.nasa.gov/learn/keywords.html

