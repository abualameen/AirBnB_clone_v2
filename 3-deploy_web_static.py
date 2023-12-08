#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to web servers.
"""

from fabric.api import run, put, env, local
from os.path import exists
from datetime import datetime


env.hosts = ['35.153.33.61', '54.165.26.200']
env.user = 'ubuntu'  # Update with your username
env.key_filename = '~/.ssh/id_rsa'  # Update with your private key path


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.
    Archive filename will include the current UTC datetime.
    """
    try:
        current_time = datetime.utcnow()
        archive_name = "web_static_{}.tgz".format(
                        current_time.strftime("%Y%m%d%H%M%S"))
        local("mkdir -p versions")
        local("tar -cvzf versions/{} web_static".format(archive_name))
        return "versions/{}".format(archive_name)
    except Exception:
        return None


def do_deploy(archive_path):
    """
    Distributes an archive to web servers.

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

        # Extract the archive to the folder /data/web_static/
        #  releases/<archive filename without extension>
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


def deploy():
    """
    Creates and distributes an archive to web servers.
    """
    archive_path = do_pack()

    if not archive_path:
        return False

    return do_deploy(archive_path)


if __name__ == "__main__":
    deploy()
