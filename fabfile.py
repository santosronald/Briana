__author__ = 'klaatu'
from fabric.api import *
from fabric.colors import green

env.user = 'admin'
env.host_string = '192.241.247.216'
env.password = 'j3it1@j9z3=dzj(2uc%5iufsxu*5r3s^xzes7%377b))wio)r6'
home_path = "/home/admin"
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
