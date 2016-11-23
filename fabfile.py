__author__ = 'klaatu'
from fabric.api import *
from fabric.colors import green

env.user = 'lfarfan'
env.host_string = '172.18.1.40'
env.password = 'Censos2017'
home_path = "/home/lfarfan/prueba"
settings = "--settings='mutacion.settings.production'"
activate_env = "source {}/brianavenv/bin/activate".format(home_path)
manage = "python manage.py"


def deploy():
    print("Beginning Deploy:")
    with cd("{}/briana".format(home_path)):
        run("git pull")
        run("{} && pip install -r requirements/base.txt".format(activate_env))
        run("{} && {} collectstatic --noinput {}".format(activate_env, manage,
                                                         settings))
        run("{} && {} migrate {}".format(activate_env, manage, settings))
        sudo("service nginx restart", pty=False)
        sudo("service supervisor restart", pty=False)
    print(green("Deploy briana successful"))


def createsuperuser():
    with cd("{}/briana".format(home_path)):
        run("{} && {} createsuperuser {}".format(activate_env, manage,
                                                 settings))
    print(green("Createsuperuser successful"))
