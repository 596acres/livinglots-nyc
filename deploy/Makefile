PORT = XXX
PROJECT_NAME = XXX
REPO_NAME = XXX
WEBAPP_NAME = xxx

env:
	easy_install-2.7 pip
	pip2.7 install --user virtualenv
	pip2.7 install --user virtualenvwrapper
	mkvirtualenv $(WEBAPP_NAME)
	pip install -r ../requirements/base.txt
	pip install -r ../requirements/production.txt

install:
	bash install node.sh
	mkdir -p $(HOME)/var
	ln -s ./deploy/admin $(HOME)/var/admin
	ln -s ./deploy/django $(HOME)/var/django
	ln -s ./deploy/supervisor $(HOME)/var/supervisor
	cat gunicorn.cfg | sed "s/<PORT>/$(PORT)/g; s/<WEBAPP_NAME>/$(WEBAPP_NAME)/g; s/<USER>/$(USER)/g;" > ../gunicorn.cfg
	cat start_gunicorn.sh | sed "s/<PORT>/$(PORT)/g; s/<REPO_NAME>/$(REPO_NAME)/g; s/<PROJECT_NAME>/$(PROJECT_NAME)/g;" > ../start_gunicorn.sh
