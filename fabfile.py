import contextlib

from fabric.api import *


env.hosts = ['fiveninesix',]
env.use_ssh_config = True


server_project_dirs = {
    'dev': '~/webapps/',
    'prod': '~/webapps/llnyc',
}

server_virtualenvs = {
    'dev': '',
    'prod': 'llnyc',
}

supervisord_programs = {
    'dev': '',
    'prod': 'llnyc',
}

supervisord_conf = '~/var/supervisor/supervisord.conf'


@contextlib.contextmanager
def cdversion(version, subdir=''):
    """cd to the version indicated"""
    with prefix('cd %s' % '/'.join([server_project_dirs[version], subdir])):
        yield


@contextlib.contextmanager
def workon(version):
    """workon the version of indicated"""
    with prefix('workon %s' % server_virtualenvs[version]):
        yield

@task
def pull(version='prod'):
    with cdversion(version):
        run('git pull --no-edit')


@task
def install_requirements(version='prod'):
    with workon(version):
        with cdversion(version):
            run('pip install -r requirements/base.txt')
            run('pip install -r requirements/production.txt')


@task
def build_static(version='prod'):
    with workon(version):
        run('django-admin collectstatic --noinput')


@task
def syncdb(version='prod'):
    with workon(version):
        run('django-admin syncdb')


@task
def restart_django(version='prod'):
    with workon(version):
        run('supervisorctl -c %s restart llnyc' % supervisord_conf)


@task
def restart_memcached():
    run('supervisorctl -c %s restart memcached' % supervisord_conf)


@task
def status():
    run('supervisorctl -c %s status' % supervisord_conf)


@task
def start(version='prod'):
    pull(version=version)
    install_requirements(version=version)
    syncdb(version=version)
    build_static(version=version)
    with workon(version):
        run('supervisorctl -c %s start %s' % (supervisord_conf,
                                              supervisord_programs[version]))


@task
def stop(version='prod'):
    with workon(version):
        run('supervisorctl -c %s stop %s' % (supervisord_conf,
                                             supervisord_programs[version]))


@task
def deploy():
    pull()
    install_requirements()
    syncdb()
    build_static()
    restart_django()
