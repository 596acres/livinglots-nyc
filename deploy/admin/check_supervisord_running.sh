#!/bin/bash

if ps -u $USER -o command | grep -v grep | grep "bin/supervisord" > /dev/null
then
    echo 'supervisord running'
else
    echo 'supervisord not running! starting now.'
    source $HOME/.bashrc
    workon $LIVING_LOTS_VIRTUAL_ENV
    supervisord -c $HOME/var/supervisor/supervisord.conf
fi
