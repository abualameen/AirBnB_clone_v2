#!/usr/bin/python3
"""
Fabric script that deletes out-of-date archives.
"""

from fabric.api import run, local, env, task
from datetime import datetime

env.hosts = ['35.153.33.61', '54.165.26.200']
env.user = 'ubuntu'  # Update with your username
env.key_filename = '~/.ssh/id_rsa'  # Update with your private key path


@task
def do_clean(number=0):
    """
    Deletes out-of-date archives.

    Args:
        number (int): Number of archives to keep. Default is 0.

    Returns:
        None
    """
    number = int(number)

    if number == 0 or number == 1:
        number = 1
    elif number == 2 or number > 2:
        number = 2

    # Delete local archives
    local("ls -1t versions | tail -n +{} | xargs -I {{}} rm versions/{{}}".format(number + 1))

    # Delete remote archives
    run("ls -1t /data/web_static/releases | tail -n +{} | xargs -I {{}} rm -rf /data/web_static/releases/{{}}".format(number + 1))

    # Remove the "total" line from the local ls output
    local("ls -ltr versions | grep -v '^total'")


# Run the clean if the script is executed directly
if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser(description="Delete out-of-date archives.")
    parser.add_argument("number", type=int, help="Number of archives to keep. Default is 0.")

    args = parser.parse_args()
    # Call the do_clean task with the specified number of archives to keep
    do_clean(args.number)
