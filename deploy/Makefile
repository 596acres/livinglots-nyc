DB_NAME = XXX
DB_PASSWORD = XXX
DB_USER = XXX
PORT = XXX
PROJECT_NAME = XXX
REPO_NAME = XXX
TILESTACHE_ALLOWED_ORIGIN = XXX
TILESTACHE_PORT = XXX
TILESTACHE_WEBAPP_NAME = XXX
WEBAPP_NAME = XXX

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

install_tilestache:
	mkdir -p $(HOME)/webapps/$(TILESTACHE_WEBAPP_NAME)/logs
	cat templates/gunicorn.cfg | sed "s/<PORT>/$(TILESTACHE_PORT)/g; s/<WEBAPP_NAME>/$(TILESTACHE_WEBAPP_NAME)/g; s/<USER>/$(USER)/g;" > $(HOME)/webapps/$(TILESTACHE_WEBAPP_NAME)/gunicorn.cfg
	cat templates/tilestache_start_gunicorn.sh | sed "s/<PORT>/$(TILESTACHE_PORT)/g; s/<WEBAPP_NAME>/$(TILESTACHE_WEBAPP_NAME)/g;" > $(HOME)/webapps/$(TILESTACHE_WEBAPP_NAME)/start_gunicorn.sh
	cat templates/tilestache.cfg | sed "s/<ALLOWED_ORIGIN>/$(TILESTACHE_ALLOWED_ORIGIN)/g; s/<DB_NAME>/$(DB_NAME)/g; s/<DB_USER>/$(DB_USER)/g; s/<DB_PASSWORD>/$(DB_PASSWORD)/g;" > $(HOME)/webapps/$(TILESTACHE_WEBAPP_NAME)/tilestache.cfg
