#!/bin/bash

#
# Load all fixtures for Living Lots NYC. DO NOT run in cron, this should only 
# be run once.
#

source $HOME/.bashrc
source $HOME/.virtualenvs/$LIVING_LOTS_VIRTUAL_ENV/bin/activate

django-admin loaddata livinglots_notify_flatblocks
django-admin loaddata livinglots_organize_flatblocks
django-admin loaddata organize_mailings_fixtures
