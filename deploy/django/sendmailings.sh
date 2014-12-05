#!/bin/bash

source $HOME/.bashrc
source $HOME/.virtualenvs/$LIVING_LOTS_VIRTUAL_ENV/bin/activate
django-admin sendmailings
