#!/bin/bash

WEBAPP_NAME="<WEBAPP_NAME>"
PORT=<PORT>
USER=$USER
GROUP=$USER
NUM_WORKERS=3
DJANGO_WSGI_MODULE=$DJANGO_PROJECT_NAME.wsgi
VIRTUALENV=$WEBAPP_NAME
LOGDIR=$HOME/webapps/$WEBAPP_NAME/logs

echo "Starting $WEBAPP_NAME"

# Activate the virtual environment
export VIRTUALENVWRAPPER_PYTHON=/usr/local/bin/python2.7
source ~/bin/virtualenvwrapper.sh
workon <VIRTUALENV>

cd $HOME/webapps/$WEBAPP_NAME

# Start Django Unicorn
exec gunicorn \
  --name $WEBAPP_NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --log-level=debug \
  --bind=127.0.0.1:$PORT \
  --log-file $LOGDIR/error.log --access-logfile $LOGDIR/access.log \
  "TileStache:WSGITileServer('$HOME/webapps/$WEBAPP_NAME/tilestache.cfg')"
