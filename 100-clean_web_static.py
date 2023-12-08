#!/usr/bin/python3
"""
Fabric script that deletes out-of-date archives.
"""

from fabric.api import env, run, local
from fabric.context_managers import cd

env.hosts = ['<IP web-01>', '<IP web-02>']
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
    local("ls -1t versions | tail -n +{} | xargs -I {{}} rm\
            versions/{{}} > /dev/null 2>&1".format(number))

    # Delete unnecessary archives in the /data/web_static/releases folder
    with cd("/data/web_static/releases"):
        run("ls -1t | tail -n +{} | xargs -I {{}} rm -rf {{}} >\
                /dev/null 2>&1".format(number))

    # Remove the "total" line from the local ls output
    local("ls -ltr versions | tail -n +2")
