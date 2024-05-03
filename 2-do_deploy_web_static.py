#!/usr/bin/python3
"""
Fabric script based on the file 2-do_deploy_web_static.py that creates and
distributes an archive to the web servers.
"""

from fabric.api import env, local, put, run
from datetime import datetime
import os

# Define the environment hosts and user for SSH
env.hosts = ["54.236.8.64", "100.24.72.30"]
env.user = 'ubuntu'

def do_pack():
    """
    Generates a .tgz archive from the contents of the 'web_static' directory.
    The archive is stored in the 'versions' directory.
    Returns:
        The path to the created archive if successful, otherwise None.
    """
    try:
        if not os.path.isdir("versions"):
            local("mkdir -p versions")
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        file_name = f"versions/web_static_{date}.tgz"
        local(f"tar -cvzf {file_name} web_static")
        return file_name
    except Exception as e:
        print(f"Error packing web_static: {e}")
        return None

def do_deploy(archive_path):
    """
    Distributes an archive to the web servers defined in the env.hosts.
    Args:
        archive_path (str): The path to the archive to deploy.
    Returns:
        True if all operations are successful, False otherwise.
    """
    if not os.path.exists(archive_path):
        print("Archive path does not exist")
        return False
    try:
        file_name = os.path.basename(archive_path)
        no_ext = file_name.split(".")[0]
        path = "/data/web_static/releases/"
        tmp_path = f"/tmp/{file_name}"

        # Upload the archive
        put(archive_path, tmp_path)

        # Create directory for the release
        run(f"mkdir -p {path}{no_ext}/")

        # Unpack the archive
        run(f"tar -xzf {tmp_path} -C {path}{no_ext}/")

        # Remove the archive from the server
        run(f"rm {tmp_path}")

        # Move unpacked content to the release directory and remove extra directory
        run(f"mv {path}{no_ext}/web_static/* {path}{no_ext}/")
        run(f"rm -rf {path}{no_ext}/web_static")

        # Update the symbolic link to point to the new release
        run("rm -rf /data/web_static/current")
        run(f"ln -s {path}{no_ext}/ /data/web_static/current")

        print("New version deployed!")
        return True
    except Exception as e:
        print(f"Deployment failed: {e}")
        return False

def deploy():
    """
    Creates and distributes an archive to the web servers.
    This function combines the processes of packing (do_pack) and deployment (do_deploy).
    Returns:
        True if the entire process is successful, False otherwise.
    """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
