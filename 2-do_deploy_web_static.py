#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers.
"""

from fabric.api import run, put, env
from os.path import exists
from datetime import datetime

env.hosts = ['35.153.33.61', '54.165.26.200']
env.user = 'ubuntu'  # Update with your username
env.key_filename = '~/.ssh/id_rsa'  # Update with your private key path


def do_deploy(archive_path):
    """
    Distributes an archive to your web servers.

    Args:
        archive_path (str): Path to the archive to deploy.

    Returns:
        bool: True if all operations have been done
        correctly, otherwise, False.
    """
    if not exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, "/tmp/")

        # Extract the archive to the folder /data/web_static
        # /releases/<archive filename without extension>
        archive_filename = archive_path.split("/")[-1]
        archive_no_extension = archive_filename.split(".")[0]
        release_path = "/data/web_static/releases/{}".format(
                        archive_no_extension)
        run("mkdir -p {}".format(release_path))
        run("tar -xzf /tmp/{} -C {}".format(archive_filename, release_path))

        # Delete the archive from the web server
        run("rm /tmp/{}".format(archive_filename))

        # Move the contents of the extracted folder to the release path
        run("mv {}/web_static/* {}".format(release_path, release_path))

        # Remove the empty web_static folder
        run("rm -rf {}/web_static".format(release_path))

        # Delete the symbolic link /data/web_static/current from the web server
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link /data/web_static/current
        run("ln -s {} /data/web_static/current".format(release_path))

        print("New version deployed!")
        return True

    except Exception as e:
        print(e)
        return False


if __name__ == "__main__":
    current_time = datetime.utcnow()
    archive_name = "web_static_{}.tgz".format(
                    current_time.strftime("%Y%m%d%H%M%S"))
    archive_path = "versions/{}".format(archive_name)
    result = do_deploy(archive_path)
    print(result)
