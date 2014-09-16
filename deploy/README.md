deploy
======

This directory contains scripts and configuration files that should make
deploying your Living Lots site simpler.

Steps
-----

1. Create a webapp folder
1. Create a database
1. Create a secrets file with the appropriate variables set
1. Load secrets file and set DJANGO_SETTINGS_MODULE on virtualenv activate
1. Edit Makefile, change all XXX values to the appropriate values
1. `make env`
1. Create a virtualenv and start working on it.
1. `make requirements`
1. `make install_admin`
