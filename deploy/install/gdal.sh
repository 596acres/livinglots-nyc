#!/bin/bash
#
# Install gdal (assumes you're on a Webfaction server)
#
GDAL_VERSION=1.11.1
VIRTUALENV=llnyc

mkdir -p ~/src/
cd ~/src/
wget http://download.osgeo.org/gdal/$GDAL_VERSION/gdal-$GDAL_VERSION.tar.gz
tar -xzf gdal-$GDAL_VERSION.tar.gz
./configure --prefix=$HOME
make
make install

export CPLUS_INCLUDE_PATH=$HOME/include/
export C_INCLUDE_PATH=$HOME/include/

workon llnyc
pip install GDAL

echo "You should now add the following to your .bashrc:"
echo "\n\texport LD_LIBRARY_PATH=$HOME/lib"
