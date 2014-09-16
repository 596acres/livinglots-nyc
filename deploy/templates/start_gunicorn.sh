#!/bin/bash

DJANGO_PROJECT_NAME="<PROJECT_NAME>"
WEBAPP_NAME="<WEBAPP_NAME>"
DJANGODIR=$HOME/webapps/$WEBAPP_NAME/$DJANGO_PROJECT_NAME
PORT=<PORT>
USER=$USER
GROUP=$USER
NUM_WORKERS=3
DJANGO_SETTINGS_MODULE=$DJANGO_PROJECT_NAME.settings.production
DJANGO_WSGI_MODULE=$DJANGO_PROJECT_NAME.wsgi
VIRTUALENV=$WEBAPP_NAME
LOGDIR=$HOME/webapps/$WEBAPP_NAME/logs

echo "Starting $WEBAPP_NAME"

# Activate the virtual environment
source ~/bin/virtualenvwrapper.sh
workon $VIRTUALENV
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE

cd $DJANGODIR

# Start Django Unicorn
exec gunicorn \
  --name $WEBAPP_NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --log-level=debug \
  --bind=127.0.0.1:$PORT \
  --log-file $LOGDIR/error.log --access-logfile $LOGDIR/access.log \
  $DJANGO_WSGI_MODULE:application
