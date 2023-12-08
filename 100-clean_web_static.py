#!/usr/bin/python3
"""
Fabric script that deletes out-of-date archives.
"""

from fabric.api import env, local
from fabric.context_managers import cd
from fabric.operations import sudo


env.hosts = ['35.153.33.61', '54.165.26.200']
env.user = 'ubuntu'  # Update with your username
env.key_filename = '~/.ssh/id_rsa'  # Update with your private key path


def do_clean(number=0):
    """
    Delete out-of-date archives.

    Args:
        number (int): The number of archives to keep.

    Returns:
        None
    """
    number = int(number)

    if number == 0 or number == 1:
        number = 1
    else:
        number += 1

    # Delete unnecessary archives in the versions folder
    with cd("/data/web_static/releases"):
        local("ls -1t versions | tail -n +{} | xargs -I {{}}\
                rm versions/{{}}".format(number))

    # Delete unnecessary archives in the /data/web_static/releases folder
    with cd("/data/web_static/releases"):
        sudo("ls -1t | tail -n +{} | xargs -I {{}} rm -rf {{}}".format(number))
