PORT = XXX
PROJECT_NAME = XXX
REPO_NAME = XXX
WEBAPP_NAME = xxx

env:
	easy_install-2.7 pip
	pip2.7 install --user virtualenv
	pip2.7 install --user virtualenvwrapper

requirements:
	pip install -r ../requirements/base.txt
	pip install -r ../requirements/production.txt

install_node:
	bash install/node.sh

install_admin:
	mkdir -p $(HOME)/var
	-ln -s $(HOME)/webapps/$(WEBAPP_NAME)/deploy/admin $(HOME)/var/admin
	-ln -s $(HOME)/webapps/$(WEBAPP_NAME)/deploy/django $(HOME)/var/django
	cat templates/gunicorn.cfg | sed "s/<PORT>/$(PORT)/g; s/<WEBAPP_NAME>/$(WEBAPP_NAME)/g; s/<USER>/$(USER)/g;" > ../gunicorn.cfg
	cat templates/start_gunicorn.sh | sed "s/<PORT>/$(PORT)/g; s/<WEBAPP_NAME>/$(WEBAPP_NAME)/g; s/<PROJECT_NAME>/$(PROJECT_NAME)/g;" > ../start_gunicorn.sh

	mkdir -p $(HOME)/var/supervisor
	cat templates/supervisord.conf | sed "s/<PORT>/$(PORT)/g; s/<WEBAPP_NAME>/$(WEBAPP_NAME)/g; s/<USER>/$(USER)/g; s/<REPO_NAME>/$(REPO_NAME)/g; s/<PROJECT_NAME>/$(PROJECT_NAME)/g;" > $(HOME)/var/supervisor/supervisord.conf
